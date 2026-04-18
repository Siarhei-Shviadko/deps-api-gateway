import asyncio
import json
import os
from functools import partial
from http import HTTPStatus
from typing import Any, Optional, Union

from async_rest_client import Methods
from cachetools import TTLCache
from fastapi.responses import Response

from deps_api_gateway.api.requests import (
    GenericPipelineRequest,
    RetryLastStepRequest,
    RunPipelineFromStepRequest,
    RunPipelineRequest,
)
from deps_api_gateway.api.responses import PipelineResponse
from deps_api_gateway.api.utilities import (
    ParsedRequest,
    ResponseBuilder,
    TypeContent,
    TypeRoutedResponse,
)
from deps_api_gateway.application.legacy import (
    ICorleone,
    IDocument,
    IDocumentTypeOld,
    IWorkflow,
)
from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    DOCUMENT_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    PLUGIN_EXTRACTION_TYPE,
    V1_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
    DocumentTypeSource,
    ExtractionType,
)
from deps_api_gateway.domain.exceptions import CompleteReviewError, PipelineError
from deps_api_gateway.infrastructure import OldGenericRestClient

from .abstract_router import AbstractRouter, RequestMapper

__all__ = ["DocumentRouter"]

EXTRACTION_STEP: str = "extraction"


class DocumentRouter(AbstractRouter):
    def __init__(
        self,
        client: OldGenericRestClient,
        document_proxy: IDocument,
        corleone_proxy: ICorleone,
        document_type_proxy: IDocumentTypeOld,
        workflow_manager_proxy: IWorkflow,
        document_type_source_cache: TTLCache,
        document_type_code_cache: TTLCache,
        document_type_extraction_type_cache: TTLCache,
        workflow_v2: bool = False,
    ) -> None:
        super().__init__(client)
        self._document_proxy = document_proxy
        self._corleone_proxy = corleone_proxy
        self._document_type_proxy = document_type_proxy
        self._workflow_manager_proxy = workflow_manager_proxy
        self._document_type_source_cache = document_type_source_cache
        self._document_type_code_cache = document_type_code_cache
        self._document_type_extraction_type_cache = document_type_extraction_type_cache
        self._workflow_v2 = workflow_v2

        if workflow_v2:
            self._logger.warning("Feature workflow V2 enabled!!!")

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (Methods.GET, rf"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/\d+$"): self._get_document,
            (Methods.GET, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents$"): self._get_documents,
            (Methods.POST, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/document-file$"): self._upload_document,
            (
                Methods.POST,
                f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/run-pipeline-from-step$",
            ): partial(self._run_appropriate_pipeline, RunPipelineFromStepRequest()),
            (Methods.POST, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/run-pipeline$"): partial(
                self._run_appropriate_pipeline, RunPipelineRequest()
            ),
            (Methods.POST, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/retry-last-step$"): partial(
                self._retry_last_step, RetryLastStepRequest()
            ),
            (Methods.POST, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/complete$"): self._complete_review,
            (Methods.POST, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/validate$"): self._validate,
            (Methods.POST, f"^{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}/documents/extract-data$"): self._extract_data,
        }

    async def _get_document(self, request: ParsedRequest) -> Response:
        response = await self._document_proxy.request(**await request.to_dict())

        if response["status_code"] == HTTPStatus.OK:
            self._cache_document_type(json.loads(response["content"]))
        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .build()
        )

    async def _get_documents(self, request: ParsedRequest) -> Response:
        response = await self._document_proxy.request(**await request.to_dict())

        if response["status_code"] == HTTPStatus.OK:
            asyncio.create_task(self._cache_document_types(json.loads(response["content"])["result"]))
        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .build()
        )

    async def _upload_document(self, request: ParsedRequest) -> Response:
        request_info = await request.to_dict()
        form = await request.form
        document_type_code = form.get("documentType")

        document_type_source = await self._get_document_type_source(document_type_code, request_info["headers"])

        if document_type_source == DocumentTypeSource.DOCUMENT_TYPE:
            extraction_type = self._get_extraction_type(document_type_code)
            response = await self._upload_document_to_workflow(form, request_info["headers"], extraction_type)
        else:
            response = await self._upload_document_to_documents(request_info, document_type_code)

        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .build()
        )

    @staticmethod
    def _get_document_id_from_document_url(url: str) -> str:
        return os.path.split(url)[-1]

    def _get_extraction_type(self, document_type_code: str) -> str:
        return self._document_type_extraction_type_cache.get(document_type_code) or PLUGIN_EXTRACTION_TYPE

    def _add_document_type_code_to_cache(self, document_id: str, code: str) -> None:
        self._document_type_code_cache[document_id] = code

    def _cache_document_type(self, document: dict[str, Any]) -> None:
        document_type_code = document.get("documentType")

        if document_type_code:
            self._add_document_type_code_to_cache(document_id=document["_id"], code=document_type_code)

    async def _cache_document_types(self, documents: list[dict[str, Any]]) -> None:
        for document in documents:
            self._cache_document_type(document)

    async def _get_document_type_source(
        self,
        document_type_code: Optional[str],
        headers: dict[str, Any],
    ) -> DocumentTypeSource:
        if not document_type_code:
            return DocumentTypeSource.CORLEONE

        cached_type_source = self._document_type_source_cache.get(document_type_code)
        if cached_type_source is not None:
            return cached_type_source

        routed_response = await self._get_document_type(document_type_code, headers)
        type_source = DocumentTypeSource.DOCUMENT_TYPE if routed_response.document_type else DocumentTypeSource.CORLEONE
        self._update_document_type_cache(routed_response.document_type or routed_response.corleone, type_source)

        return type_source

    def _update_document_type_cache(self, document_type: TypeContent, source: DocumentTypeSource) -> None:
        self._document_type_source_cache[document_type.code] = source
        self._document_type_extraction_type_cache[document_type.code] = document_type.extraction_type

    async def _get_document_type(self, document_type_code: str, headers: dict[str, Any]) -> TypeRoutedResponse:
        corleone_url = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/types/{document_type_code}"
        document_type_url = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}/types/{document_type_code}"

        task_corleone = self._corleone_proxy.get_document_type(
            method=Methods.GET,
            url=corleone_url,
            query="",
            headers=headers,
            data=b"",
        )
        task_document_type = self._document_type_proxy.get_document_type(
            method=Methods.GET,
            url=document_type_url,
            query="",
            headers=headers,
            data=b"",
        )

        corleone_task_result, document_type_task_result = await asyncio.gather(
            asyncio.create_task(task_corleone),
            asyncio.create_task(task_document_type),
            return_exceptions=True,
        )

        return TypeRoutedResponse(
            corleone_task_result=corleone_task_result, document_type_task_result=document_type_task_result  # type: ignore
        )

    async def _upload_document_to_documents(self, request_info: dict[str, Any], document_type_code: str) -> dict:
        document_response = await self._document_proxy.upload_document(**request_info)
        document_id = json.loads(document_response["content"])["id"]

        self._add_document_type_code_to_cache(document_id, document_type_code)

        return document_response

    async def _upload_document_to_workflow(
        self,
        form: dict[str, Any],
        headers: dict[str, Any],
        extraction_type: str,
    ) -> dict:
        if self._workflow_v2:
            return await self._upload_document_with_workflow_v2(form=form, headers=headers)

        return await self._upload_document_with_workflow(form=form, headers=headers, extraction_type=extraction_type)

    async def _upload_document_with_workflow(
        self,
        form: dict[str, Any],
        headers: dict[str, Any],
        extraction_type: str,
    ) -> dict:
        if extraction_type == ExtractionType.PROTOTYPE:
            raise NotImplementedError("Prototype extraction with workflow v1 is not implemented")

        url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/{extraction_type}-processing-workflow"
        file = form.get("file")

        return await self._workflow_manager_proxy.upload_document(url, form, file, headers)

    async def _upload_document_with_workflow_v2(self, form: dict[str, Any], headers: dict[str, Any]) -> dict:
        return await self._workflow_manager_proxy.upload_document_v2(form=form, headers=headers)

    async def _run_appropriate_pipeline(
        self,
        request: Union[RunPipelineRequest, RunPipelineFromStepRequest],
        original_request: ParsedRequest,
    ) -> Response:
        request.original_request = original_request
        doc_ids = list((await request.original_request.json_data)["documentIds"])
        await self._prepare_pipeline_requests_for_docs(request, doc_ids)
        return await self._make_pipeline_requests(request)

    async def _retry_last_step(self, request: RetryLastStepRequest, original_request: ParsedRequest) -> Response:
        request.original_request = original_request
        doc_id = (await request.original_request.json_data)["documentId"]
        await self._prepare_pipeline_requests_for_docs(request, [doc_id])

        return await self._make_pipeline_requests(request)

    async def _extract_data(self, request: ParsedRequest):
        data = await request.json_data
        data["step"] = EXTRACTION_STEP
        await request.change_body(json.dumps(data).encode("utf-8"))
        await self._run_appropriate_pipeline(RunPipelineFromStepRequest(), request)
        document_requests = [
            self._build_get_document_request(request.headers, doc_id) for doc_id in data["documentIds"]
        ]
        document_responses = await asyncio.gather(
            *(self._document_proxy.request(**doc_req) for doc_req in document_requests),
        )
        return (
            ResponseBuilder()
            .with_content(
                [
                    json.loads(document_detail["content"])
                    for document_detail in document_responses
                    if document_detail["status_code"] < HTTPStatus.BAD_REQUEST
                ],
            )
            .build()
        )

    async def _complete_review(self, request: ParsedRequest) -> Response:  # noqa: WPS217
        doc_id = (await request.json_data)["documentId"]
        doc_type_source = await self._get_document_type_source_by_document_id(doc_id, request.headers)
        if doc_type_source == DocumentTypeSource.CORLEONE:
            self._logger.debug("Send complete review request to the document service.")
            response = await self._document_proxy.request(**await request.to_dict())
            return (
                ResponseBuilder()
                .with_content(response["content"])
                .with_status(response["status_code"])
                .with_headers(response["headers"])
                .build()
            )

        self._logger.debug("Send complete review request to the workflow-manager")
        response = await self._workflow_manager_proxy.request(
            **await request.change_url(
                request.url, f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/complete-review-workflow"
            ).to_dict(),
        )
        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .build()
        )

    async def _validate(self, request: ParsedRequest) -> Response:  # noqa: WPS217
        doc_id = (await request.json_data)["documentId"]
        doc_type_source = await self._get_document_type_source_by_document_id(doc_id, request.headers)
        if doc_type_source == DocumentTypeSource.CORLEONE:
            self._logger.debug("Send validate request to the document service.")
            return Response(**await self._document_proxy.request(**await request.to_dict()))

        self._logger.debug("Send validate request to the workflow-manager")
        response = await self._workflow_manager_proxy.request(
            **await request.change_url(
                request.url, f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/validate-workflow"
            ).to_dict(),
        )
        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .build()
        )

    async def _get_document_info_by_id(self, headers: dict[str, Any], doc_id: str) -> dict[str, Any]:
        document_response = await self._document_proxy.request(**self._build_get_document_request(headers, doc_id))
        if document_response["status_code"] == HTTPStatus.OK:
            response_content = json.loads(document_response["content"])
            self._cache_document_type(response_content)
            return response_content
        self._logger.error(
            f"Request to the document service failed. Status_code: {document_response['status_code']}, "
            + f"content: {document_response['content']}"
        )
        raise CompleteReviewError(
            f"Request to the document service returns with {document_response['status_code']} status_code"
        )

    async def _prepare_pipeline_requests_for_docs(self, request: GenericPipelineRequest, doc_ids: list[str]) -> None:
        requests_to_document = [
            self._build_get_document_request(request.original_request.headers, doc_id) for doc_id in doc_ids
        ]

        pipeline_sources = [
            asyncio.create_task(self._choose_pipeline_source(request, req)) for req in requests_to_document
        ]
        for source in asyncio.as_completed(pipeline_sources):
            result = await source  # noqa: WPS110
            self._logger.debug(
                "Document with id %s added to %s %s pipeline"
                % (result["doc_id"], result["source"], result["extraction_type"])
            )
            await request.update_request(**result)
        request.serialize_data()

    async def _choose_pipeline_source(
        self, request: GenericPipelineRequest, request_to_doc: dict[str, Any]
    ) -> dict[str, Any]:
        response = await self._document_proxy.request(**request_to_doc)
        if response["status_code"] != HTTPStatus.OK:
            self._logger.error("Choose pipeline source failed with error. %s" % response)
            raise PipelineError(json.loads(response["content"]))

        document = json.loads(response["content"])
        doc_type_code = document["documentType"]
        doc_type_source = await self._get_document_type_source(doc_type_code, request_to_doc["headers"])

        extraction_type = (
            self._get_extraction_type(doc_type_code) if doc_type_source == DocumentTypeSource.DOCUMENT_TYPE else None
        )

        source = request.doc_type_pipeline_mapper[doc_type_source]

        return {"doc_id": document["_id"], "source": source, "extraction_type": extraction_type}

    async def _make_pipeline_requests(self, request: GenericPipelineRequest) -> Response:
        if req := request.document_pipeline_request:
            request.document_request_task = self._document_proxy.request(**req)
        if req := request.workflow_manager_pipeline_request:
            request.workflow_request_task = self._workflow_manager_proxy.request(**req)

        await asyncio.wait(request.get_pipeline_tasks())

        response = PipelineResponse(
            document_response=request.document_request_task,
            workflow_response=request.workflow_request_task,
        )
        return ResponseBuilder().with_content(response.content).with_status(HTTPStatus.ACCEPTED).build()

    @staticmethod
    def _build_get_document_request(headers: dict[str, Any], doc_id: str) -> dict[str, Any]:
        return {
            "method": Methods.GET,
            "url": f"/api/document/v1/documents/{doc_id}",
            "query": "",
            "headers": headers,
            "data": b"",
        }

    async def _get_document_type_source_by_document_id(
        self,
        doc_id: str,
        headers: dict[str, Any],
    ) -> DocumentTypeSource:
        doc_type = (
            self._document_type_code_cache.get(doc_id)
            or (await self._get_document_info_by_id(headers, doc_id))["documentType"]
        )
        return await self._get_document_type_source(doc_type, headers)
