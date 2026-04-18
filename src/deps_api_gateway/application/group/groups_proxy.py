from typing import Optional, Protocol

from ..proxy_response import ProxyResponse

__all__ = ["IGroupsProxy"]


class IGroupsProxy(Protocol):
    async def get_groups(
        self,
        name: Optional[str],
        document_type_id: Optional[str],
        date_start: Optional[str],
        date_end: Optional[str],
        page: Optional[int],
        per_page: Optional[int],
        sort_by: str,
        sort_order: str,
    ) -> ProxyResponse:
        pass

    async def get_group(
        self,
        group_id: str,
    ) -> ProxyResponse:
        pass

    async def create_group(
        self,
        name: str,
        document_type_ids: list[str],
    ) -> ProxyResponse:
        pass

    async def delete_groups(self, ids: list[str]) -> ProxyResponse:
        pass

    async def add_document_types(self, group_id: str, document_type_ids: list[str]) -> ProxyResponse:
        pass

    async def remove_document_types(self, group_id: str, document_type_ids: list[str]) -> ProxyResponse:
        pass

    async def update_group_info(self, group_id: str, name: str) -> ProxyResponse:
        pass
