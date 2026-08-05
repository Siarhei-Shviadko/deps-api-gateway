from typing import Optional, Protocol

from ..proxy_response import ProxyResponse

__all__ = ["ISplittingProxy"]


class ISplittingProxy(Protocol):
    async def find_splitters(self, group_id: str | None = None) -> ProxyResponse:
        pass

    async def find_splitter_for(self, group_id: str, document_type_id: Optional[str]) -> ProxyResponse:
        pass

    async def find_splitter(self, splitter_id: str) -> ProxyResponse:
        pass

    async def create_splitter(self, data: dict) -> ProxyResponse:
        pass

    async def update_splitter(self, splitter_id: str, data: dict) -> ProxyResponse:
        pass

    async def remove_splitter(self, splitter_id: str) -> ProxyResponse:
        pass

    async def get_proposal(self, proposal_id: str) -> ProxyResponse:
        pass

    async def update_proposal(self, proposal_id: str, data: dict) -> ProxyResponse:
        pass

    async def confirm_proposal(self, proposal_id: str) -> ProxyResponse:
        pass
