from datetime import datetime
from typing import Any, Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    FileCreationData,
    IBatchProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import FILES_BATCH_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import BatchServiceUnavailableError

__all__ = ["BatchProxy"]


class BatchProxy(GenericRestClient, IBatchProxy):
    exception = BatchServiceUnavailableError
    v1_prefix = f"{FILES_BATCH_BASE_API_PREFIX}{V1_PREFIX}"

    async def get_batches(
        self,
        name: Optional[str],
        status: Optional[list[str]],
        group: Optional[str],
        date_start: Optional[datetime],
        date_end: Optional[datetime],
        page: Optional[int],
        per_page: Optional[int],
        sort_by: str,
        sort_order: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/batches"

        data: dict[str, Any] = {
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        if name is not None:
            data["name"] = name

        if status is not None:
            data["status"] = status

        if group is not None:
            data["group"] = group

        if date_start is not None:
            data["dateStart"] = date_start

        if date_end is not None:
            data["dateEnd"] = date_end

        if page is not None:
            data["page"] = page

        if per_page is not None:
            data["perPage"] = per_page

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=url,
                    params=data,
                )
            )

    async def create_batch(
        self,
        batch_name: str,
        group_id: Optional[str],
        file_params: list[FileCreationData],
        batch_metadata: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/batches"

        files_data = [
            {
                "name": fp.name,
                "path": fp.path,
                "documentTypeId": fp.document_type_id,
                "processingParams": {
                    "engine": fp.processing_params.engine,
                    "language": fp.processing_params.language,
                    "llmType": fp.processing_params.llm_type,
                    "parsingFeatures": fp.processing_params.parsing_features,
                },
            }
            for fp in file_params
        ]

        data: dict[str, Any] = {
            "name": batch_name,
            "groupId": group_id,
            "metadata": batch_metadata,
            "files": files_data,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=url,
                    json=data,
                )
            )

    async def find_batch(self, batch_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.v1_prefix}/batches/{batch_id}"),
            )

    async def delete_batches(self, ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.v1_prefix}/batches",
                    params={"ids": ids},
                ),
            )

    async def delete_batches_with_documents(self, ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.v1_prefix}/batches/with-documents",
                    params={"ids": ids},
                ),
            )

    async def delete_files(self, batch_id: str, file_ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.v1_prefix}/batches/{batch_id}/files",
                    params={"ids": file_ids},
                ),
            )

    async def delete_files_with_documents(self, batch_id: str, file_ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.v1_prefix}/batches/{batch_id}/files/with-documents",
                    params={"ids": file_ids},
                ),
            )

    async def add_files(self, batch_id: str, files: list[dict[str, Any]]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.v1_prefix}/batches/{batch_id}/files",
                    json={"files": files},
                ),
            )

    async def update_batch(self, batch_id: str, name: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v1_prefix}/batches/{batch_id}",
                    json={"name": name},
                )
            )
