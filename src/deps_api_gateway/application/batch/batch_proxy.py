from datetime import datetime
from typing import Any, Optional, Protocol

from ..proxy_response import ProxyResponse
from .file_creation_data import FileCreationData

__all__ = ["IBatchProxy"]


class IBatchProxy(Protocol):
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
        pass

    async def create_batch(
        self,
        batch_name: str,
        group_id: Optional[str],
        file_params: list[FileCreationData],
        batch_metadata: Optional[dict[str, Any]] = None,
    ) -> ProxyResponse:
        pass

    async def find_batch(self, batch_id: str) -> ProxyResponse:
        pass

    async def delete_batches(self, ids: list[str]) -> ProxyResponse:
        pass

    async def delete_batches_with_documents(self, ids: list[str]) -> ProxyResponse:
        pass

    async def delete_files(self, batch_id: str, file_ids: list[str]) -> ProxyResponse:
        pass

    async def delete_files_with_documents(self, batch_id: str, file_ids: list[str]) -> ProxyResponse:
        pass

    async def add_files(self, batch_id: str, files: list[dict[str, Any]]) -> ProxyResponse:
        pass

    async def update_batch(self, batch_id: str, name: str) -> ProxyResponse:
        pass
