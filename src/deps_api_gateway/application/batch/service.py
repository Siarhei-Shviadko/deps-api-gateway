from datetime import datetime
from typing import Any, Optional

from ..proxy_response import ProxyResponse
from .batch_proxy import IBatchProxy
from .file_creation_data import FileCreationData

__all__ = ["BatchService"]


class BatchService:
    def __init__(
        self,
        batch_proxy: IBatchProxy,
    ) -> None:
        self._batch_proxy = batch_proxy

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
        return await self._batch_proxy.get_batches(
            name=name,
            status=status,
            group=group,
            date_start=date_start,
            date_end=date_end,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    async def create_batch(
        self,
        batch_name: str,
        group_id: Optional[str],
        file_params: list[FileCreationData],
        batch_metadata: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        return await self._batch_proxy.create_batch(
            batch_name=batch_name,
            group_id=group_id,
            file_params=file_params,
            batch_metadata=batch_metadata,
        )

    async def find_batch(self, batch_id: str) -> ProxyResponse:
        return await self._batch_proxy.find_batch(batch_id)

    async def delete_batches(self, ids: list[str]) -> ProxyResponse:
        return await self._batch_proxy.delete_batches(ids)

    async def delete_batches_with_documents(self, ids: list[str]) -> ProxyResponse:
        return await self._batch_proxy.delete_batches_with_documents(ids)

    async def delete_files(self, batch_id: str, file_ids: list[str]) -> ProxyResponse:
        return await self._batch_proxy.delete_files(batch_id=batch_id, file_ids=file_ids)

    async def delete_files_with_documents(self, batch_id: str, file_ids: list[str]) -> ProxyResponse:
        return await self._batch_proxy.delete_files_with_documents(batch_id=batch_id, file_ids=file_ids)

    async def add_files(self, batch_id: str, files: list[dict[str, Any]]) -> ProxyResponse:
        return await self._batch_proxy.add_files(batch_id=batch_id, files=files)

    async def update_batch(self, batch_id: str, name: str) -> ProxyResponse:
        return await self._batch_proxy.update_batch(batch_id=batch_id, name=name)
