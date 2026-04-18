import json
from typing import Any, Optional

from aiohttp import FormData
from async_rest_client import Methods
from starlette.datastructures import UploadFile

from deps_api_gateway.application import (
    IWorkflowManagerProxy,
    NeedsReviewOption,
    ParsingFeature,
    ProxyResponse,
    ProxyResponseFactory,
    Status,
    WorkflowConfiguration,
)
from deps_api_gateway.constants import (
    V1_PREFIX,
    V2_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)

from ..generic_rest_client import GenericRestClient
from .exceptions import WorkflowManagerServiceUnavailableError

__all__ = ["WorkflowManagerProxy"]


class WorkflowManagerProxy(GenericRestClient, IWorkflowManagerProxy):
    v1_prefix = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V2_PREFIX}"
    exception = WorkflowManagerServiceUnavailableError

    async def run_pipeline_from_step(
        self,
        document_ids: list[str],
        step: Status,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        llm_type: Optional[str] = None,
        parsing_features: Optional[set[ParsingFeature]] = None,
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/run-pipeline-from-step"

        data = {
            "documentIds": document_ids,
            "step": step,
        }

        if engine is not None:
            data["engineName"] = engine
        if language is not None:
            data["language"] = language
        if llm_type is not None:
            data["llmType"] = llm_type
        if parsing_features is not None:
            data["parsingFeatures"] = list(parsing_features)

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def create_template(
        self,
        name: str,
        language: str,
        engine: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/template-workflow"

        data = {
            "name": name,
            "language": language,
            "engine": engine,
        }
        if description is not None:
            data["description"] = description
        if group_id is not None:
            data["groupId"] = group_id

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def create_template_from(
        self,
        src_template_id: str,
        name: str,
        language: str,
        engine: str,
        description: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/template-workflow/from"

        data = {
            "copyFrom": src_template_id,
            "name": name,
            "language": language,
            "engine": engine,
        }
        if description is not None:
            data["description"] = description
        if group_id is not None:
            data["groupId"] = group_id

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def create_template_version(
        self,
        document_type_id: str,
        files: list[UploadFile],
        name: str,
        description: Optional[str] = None,
        markup_automatically: bool = False,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/template-workflow/{document_type_id}/versions"

        form_data = FormData()

        for file in files:
            form_data.add_field(
                "files",
                await file.read(),
                filename=file.filename,
                content_type=file.content_type,
            )
        form_data.add_field("name", name)
        if description is not None:
            form_data.add_field("description", description)
        if markup_automatically is not None:
            form_data.add_field("markupAutomatically", str(markup_automatically))
        data = form_data()

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, data=data))

    async def upload_document(
        self,
        document_name: str,
        file: UploadFile,
        document_type_id: Optional[str],
        engine: Optional[str],
        language: Optional[str],
        llm_type: Optional[str],
        parsing_features: list[str],
        needs_unifier: bool,
        needs_extraction: bool,
        assign_to_me: bool,
        metadata: Optional[dict[str, Any]],
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/upload-document"

        request = {
            "documentName": document_name,
            "documentType": document_type_id,
            "engine": engine,
            "language": language,
            "llmType": llm_type,
            "parsingFeatures": json.dumps(parsing_features),
            "needsUnifier": str(needs_unifier),
            "needsExtraction": str(needs_extraction),
            "assignedToMe": str(assign_to_me),
            "metadata": json.dumps(metadata) if metadata is not None else metadata,
        }

        form_data = FormData({key: value for key, value in request.items() if value is not None})
        form_data.add_field(
            "file",
            await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data()),
            )

    async def import_documents(
        self,
        paths: list[str],
        source: str,
        document_type_id: Optional[str],
        engine: Optional[str],
        language: Optional[str],
        llm_type: Optional[str],
        parsing_features: list[str],
        needs_unifier: bool,
        needs_extraction: bool,
        assign_to_me: bool,
        needs_parsing: Optional[bool] = None,
        needs_validation: Optional[bool] = None,
        needs_review: Optional[NeedsReviewOption] = None,
        needs_output_exporting: Optional[bool] = None,
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/import-documents"

        data = {
            "paths": paths,
            "source": source,
            "documentType": document_type_id,
            "engine": engine,
            "language": language,
            "llmType": llm_type,
            "parsingFeatures": parsing_features,
            "invokeUnifier": needs_unifier,
            "invokeExtraction": needs_extraction,
            "invokeParsing": needs_parsing,
            "invokeValidation": needs_validation,
            "needsReview": needs_review.value if needs_review is not None else None,
            "invokeOutputExporting": needs_output_exporting,
            "assignedToMe": assign_to_me,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def validate_document(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/validate-workflow"

        data = {"documentId": document_id}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def retry_last_failed_step(self, document_id: str) -> ProxyResponse:
        url = f"{self.v2_prefix}/retry-pipeline-last-step"

        data = {"documentId": document_id}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def run_from_first_step(self, document_id: str) -> ProxyResponse:
        url = f"{self.v2_prefix}/run-pipeline"

        data = {"documentId": document_id}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def complete_review(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/complete-review-workflow"

        data = {"documentId": document_id}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def get_saga_state(self, entity_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/sagas/{entity_id}/state"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def get_workflow_configuration(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/workflow-configuration/{document_type_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def get_workflow_configurations(self) -> ProxyResponse:
        url = f"{self.v1_prefix}/workflow-configuration"
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def update_workflow_configuration(self, workflow_configuration: WorkflowConfiguration) -> ProxyResponse:
        url = f"{self.v1_prefix}/workflow-configuration"

        payload = {key: value for key, value in workflow_configuration.items() if value is not None}
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=payload)
            )
