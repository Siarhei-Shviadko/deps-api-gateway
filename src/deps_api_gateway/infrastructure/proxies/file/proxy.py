import json
from datetime import datetime
from typing import Any

from aiohttp import FormData
from async_rest_client import Methods
from fastapi import UploadFile

from deps_api_gateway.application import ProxyResponse, ProxyResponseFactory
from deps_api_gateway.application.file import IFileProxy
from deps_api_gateway.constants import (
    FILES_BASE_API_PREFIX,
    FILES_ROUTER_PREFIX,
    V1_PREFIX,
)

from ..generic_rest_client import GenericRestClient
from .exceptions import FileServiceUnavailableError

__all__ = ["FileProxy"]


class FileProxy(GenericRestClient, IFileProxy):
    exception = FileServiceUnavailableError
    v1_prefix = f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}"

    async def get_files(
        self,
        name: str | None,
        state: list[str] | None,
        labels: list[str] | None,
        date_start: datetime | None,
        date_end: datetime | None,
        page: int | None,
        per_page: int | None,
        sort_by: str,
        sort_order: str,
        reference_available: bool | None,
        reference: str | None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}"

        data: dict[str, Any] = {
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        if name is not None:
            data["name"] = name

        if state is not None:
            data["state"] = state

        if labels is not None:
            data["labels"] = labels

        if date_start is not None:
            data["dateStart"] = date_start

        if date_end is not None:
            data["dateEnd"] = date_end

        if page is not None:
            data["page"] = page

        if per_page is not None:
            data["perPage"] = per_page

        if reference_available is not None:
            data["referenceAvailable"] = json.dumps(reference_available)

        if reference is not None:
            data["reference"] = reference

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url, params=data))

    async def get_file(self, file_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/{file_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def process_file(
        self,
        file: UploadFile,
        labels: list[str] | None,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/process"

        form_data = FormData()
        form_data.add_field(
            "file",
            await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )
        form_data.add_field("needsUnifier", str(needs_unifier))
        form_data.add_field("needsExtraction", str(needs_extraction))
        form_data.add_field("assignedToMe", str(assigned_to_me))

        if engine is not None:
            form_data.add_field("engine", engine)
        if language is not None:
            form_data.add_field("language", language)
        if llm_type is not None:
            form_data.add_field("llmType", llm_type)
        if parsing_features is not None:
            form_data.add_field("parsingFeatures", json.dumps(parsing_features))
        if labels is not None:
            form_data.add_field("labels", json.dumps(labels))
        if metadata is not None:
            form_data.add_field("metadata", json.dumps(metadata))

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data())
            )

    async def classify_file(
        self,
        file: UploadFile,
        group_id: str,
        labels: list[str] | None,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/classify"

        form_data = FormData()
        form_data.add_field(
            "file",
            await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )
        form_data.add_field("groupId", group_id)
        form_data.add_field("needsUnifier", str(needs_unifier))
        form_data.add_field("needsExtraction", str(needs_extraction))
        form_data.add_field("assignedToMe", str(assigned_to_me))

        if engine is not None:
            form_data.add_field("engine", engine)
        if language is not None:
            form_data.add_field("language", language)
        if llm_type is not None:
            form_data.add_field("llmType", llm_type)
        if parsing_features is not None:
            form_data.add_field("parsingFeatures", json.dumps(parsing_features))
        if labels is not None:
            form_data.add_field("labels", json.dumps(labels))
        if metadata is not None:
            form_data.add_field("metadata", json.dumps(metadata))

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data())
            )

    async def classify_existing_file(
        self,
        file_id: str,
        group_id: str,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{file_id}/classify"

        request = {
            "groupId": group_id,
            "engine": engine,
            "language": language,
            "llmType": llm_type,
            "parsingFeatures": parsing_features,
            "needsUnifier": needs_unifier,
            "needsExtraction": needs_extraction,
            "assignedToMe": assigned_to_me,
            "metadata": metadata,
        }
        request_filtered = {k: v for k, v in request.items() if v is not None}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=request_filtered)
            )

    async def split_file(
        self,
        file: UploadFile,
        document_type_id: str | None,
        classification_enabled: bool,
        group_id: str,
        labels: list[str] | None,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        needs_splitting_proposal_review: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/split"

        form_data = FormData()
        form_data.add_field(
            "file",
            await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )
        form_data.add_field("groupId", group_id)
        form_data.add_field("classificationEnabled", str(classification_enabled))
        form_data.add_field("needsUnifier", str(needs_unifier))
        form_data.add_field("needsExtraction", str(needs_extraction))
        form_data.add_field("assignedToMe", str(assigned_to_me))
        form_data.add_field("needsSplittingProposalReview", str(needs_splitting_proposal_review))

        if document_type_id is not None:
            form_data.add_field("documentTypeId", document_type_id)
        if engine is not None:
            form_data.add_field("engine", engine)
        if language is not None:
            form_data.add_field("language", language)
        if llm_type is not None:
            form_data.add_field("llmType", llm_type)
        if parsing_features is not None:
            form_data.add_field("parsingFeatures", json.dumps(parsing_features))
        if labels is not None:
            form_data.add_field("labels", json.dumps(labels))
        if metadata is not None:
            form_data.add_field("metadata", json.dumps(metadata))

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data())
            )

    async def split_existing_file(
        self,
        file_id: str,
        document_type_id: str | None,
        classification_enabled: bool,
        group_id: str,
        engine: str | None,
        language: str | None,
        llm_type: str | None,
        parsing_features: list[str] | None,
        needs_unifier: bool,
        needs_extraction: bool,
        assigned_to_me: bool,
        needs_splitting_proposal_review: bool,
        metadata: dict[str, Any] | None = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{file_id}/split"

        request = {
            "documentTypeId": document_type_id,
            "groupId": group_id,
            "classificationEnabled": classification_enabled,
            "engine": engine,
            "language": language,
            "llmType": llm_type,
            "parsingFeatures": parsing_features,
            "needsUnifier": needs_unifier,
            "needsExtraction": needs_extraction,
            "assignedToMe": assigned_to_me,
            "needsSplittingProposalReview": needs_splitting_proposal_review,
            "metadata": metadata,
        }
        request_filtered = {k: v for k, v in request.items() if v is not None}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PATCH, url=url, json=request_filtered)
            )

    async def delete_files(self, ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params={"ids": ids})
            )

    async def create_document_from_file(
        self,
        file_id: str,
        document_type_id: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{file_id}/create-document"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, json={"documentTypeId": document_type_id})
            )

    async def create_batch_from_file(
        self,
        file_id: str,
        batch_name: str,
        batch_files: list[dict[str, Any]],
        group_id: str | None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{file_id}/create-batch"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=url,
                    json={"batchName": batch_name, "files": batch_files, "groupId": group_id},
                )
            )

    async def restart_file(self, file_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/{file_id}/restart"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url))
