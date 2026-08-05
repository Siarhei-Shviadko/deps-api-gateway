from typing import Optional

from ..proxy_response import ProxyResponse
from .splitter_proxy import ISplittingProxy

__all__ = ["SplittingService"]


class SplittingService:
    def __init__(self, splitter_proxy: ISplittingProxy) -> None:
        self._splitter_proxy = splitter_proxy

    async def find_splitters(self, group_id: str | None = None) -> ProxyResponse:
        return await self._splitter_proxy.find_splitters(group_id=group_id)

    async def find_splitter_for(self, group_id: str, document_type_id: Optional[str]) -> ProxyResponse:
        return await self._splitter_proxy.find_splitter_for(
            group_id=group_id,
            document_type_id=document_type_id,
        )

    async def find_splitter(self, splitter_id: str) -> ProxyResponse:
        return await self._splitter_proxy.find_splitter(splitter_id=splitter_id)

    async def create_splitter(self, data: dict) -> ProxyResponse:
        return await self._splitter_proxy.create_splitter(data=data)

    async def update_splitter(self, splitter_id: str, data: dict) -> ProxyResponse:
        return await self._splitter_proxy.update_splitter(splitter_id=splitter_id, data=data)

    async def remove_splitter(self, splitter_id: str) -> ProxyResponse:
        return await self._splitter_proxy.remove_splitter(splitter_id=splitter_id)

    async def get_proposal(self, proposal_id: str) -> ProxyResponse:
        return await self._splitter_proxy.get_proposal(proposal_id=proposal_id)

    async def update_proposal(self, proposal_id: str, data: dict) -> ProxyResponse:
        return await self._splitter_proxy.update_proposal(proposal_id=proposal_id, data=data)

    async def confirm_proposal(self, proposal_id: str) -> ProxyResponse:
        return await self._splitter_proxy.confirm_proposal(proposal_id=proposal_id)
