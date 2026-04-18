import json
from typing import Any, Optional

from aiohttp import FormData
from async_rest_client import Methods
from starlette.datastructures import UploadFile

from deps_api_gateway.application import (
    DocumentListFilterData,
    IDocumentProxy,
    NeedsReviewOption,
    PartialUpdateDocumentData,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import DOCUMENT_BASE_API_PREFIX, V1_PREFIX, V2_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import DocumentsServiceUnavailableError

__all__ = ["DocumentProxy"]


class DocumentProxy(GenericRestClient, IDocumentProxy):
    v1_prefix = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{DOCUMENT_BASE_API_PREFIX}{V2_PREFIX}"

    async def get_document_list(self, filter_data: DocumentListFilterData) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents"

        data: dict = filter_data
        if (datetime_range := data.get("dateRange")) is not None:
            data["dateRange"] = json.dumps([date.isoformat() for date in datetime_range])
        if (states := data.get("states")) is not None:
            data["states"] = json.dumps(states)
        if (types := data.get("types")) is not None:
            data["types"] = json.dumps(types)
        if (except_types := data.get("exceptTypes")) is not None:
            data["exceptTypes"] = json.dumps(except_types)
        if (engines := data.get("engines")) is not None:
            data["engines"] = json.dumps(engines)
        if (labels := data.get("labels")) is not None:
            data["labels"] = json.dumps(labels)
        if (groups := data.get("groups")) is not None:
            data["groups"] = json.dumps(groups)
        if (filter_ids := data.get("filterIds")) is not None:
            data["filterIds"] = json.dumps(filter_ids)
        if (has_reviewer := data.get("hasReviewer")) is not None:
            data["hasReviewer"] = json.dumps(has_reviewer)
        if (sorting_field := data.get("sortField")) is not None:
            data["sortField"] = sorting_field.value
        if (sorting_direction := data.get("sortDirect")) is not None:
            data["sortDirect"] = sorting_direction.value
        if (parent_id := data.get("parentId")) is not None:
            data["parentId"] = parent_id

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url, params=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def get_document_detail(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/{document_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def partial_update_document(
        self, document_id: str, document_data: PartialUpdateDocumentData
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/{document_id}"

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=document_data)
            )
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def delete_document_list(
        self,
        document_ids: list[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents"

        data = {"documentIds": document_ids}

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, json=data)
            )
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def add_comment(self, document_id: str, text: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/add-comment"

        data = {"documentId": document_id, "text": text}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def get_labels(self) -> ProxyResponse:
        url = f"{self.v1_prefix}/labels"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def remove_label_from_document(self, document_id: str, label_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/remove-label"

        data = {"documentId": document_id, "labelId": label_id}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def create_label(self, label_name: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/labels"

        data = {"labelName": label_name}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def add_label_on_document(self, document_id: str, label_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/add-label"

        data = {"documentIds": [document_id], "labelId": label_id}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def add_label_on_documents_batch(self, document_ids: list[str], label_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/add-label"

        data = {"documentIds": document_ids, "labelId": label_id}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def get_document_states(self) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/states"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def get_document_metadata(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/{document_id}/metadata"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def download_original_files(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/{document_id}/files"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def download_preprocessed_files(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/{document_id}/preprocessed-images"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def start_review(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/start-review"

        data = {"documentIds": [document_id]}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def assign_type(self, document_id: str, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/assign-type"

        data = {"documentIds": [document_id], "typeName": document_type_id}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def create_document(
        self,
        document_name: str,
        file: UploadFile,
        document_type_id: Optional[str] = None,
        group_id: Optional[str] = None,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        llm_type: Optional[str] = None,
        parsing_features: Optional[list[str]] = None,
        needs_unification: bool = True,
        needs_extraction: bool = True,
        needs_parsing: Optional[bool] = None,
        needs_validation: Optional[bool] = None,
        needs_review: Optional[NeedsReviewOption] = None,
        needs_output_exporting: Optional[bool] = None,
        assign_to_me: bool = False,
        metadata: Optional[dict[str, Any]] = None,
        label_ids: Optional[list[str]] = None,
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/documents"

        data = {
            "documentName": document_name,
            "documentType": document_type_id,
            "groupId": group_id,
            "engine": engine,
            "language": language,
            "llmType": llm_type,
            "needsUnifier": str(needs_unification),
            "needsExtraction": str(needs_extraction),
            "needsParsing": str(needs_parsing) if needs_parsing is not None else None,
            "needsValidation": str(needs_validation) if needs_validation is not None else None,
            "needsReview": needs_review.value if needs_review is not None else None,
            "needsOutputExporting": str(needs_output_exporting) if needs_output_exporting is not None else None,
            "parsingFeatures": json.dumps(parsing_features) if parsing_features is not None else None,
            "metadata": json.dumps(metadata) if metadata else None,
            "assignedToMe": str(assign_to_me),
            "labelIds": json.dumps(label_ids) if label_ids else None,
        }

        form_data = FormData({key: value for key, value in data.items() if value is not None})
        form_data.add_field(
            "file",
            await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data()),
            )

        except Exception as error:
            raise DocumentsServiceUnavailableError(error)

    async def extract_data(self, document_ids: list[str], engine: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/documents/extract-data"
        data = {
            "documentIds": document_ids,
            "engineName": engine,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise DocumentsServiceUnavailableError(error)
