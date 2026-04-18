from typing import Protocol

from ..proxy_response import ProxyResponse
from ..types.agentic_ai.arguments import ContextArguments

__all__ = ["IAgenticAIProxy"]


class IAgenticAIProxy(Protocol):
    async def create_agent_vendor(
        self,
        name: str,
        description: str,
        base_url: str,
        avatar_url: str | None = None,
    ) -> ProxyResponse:
        pass

    async def get_agent_vendors(self) -> ProxyResponse:
        pass

    async def activate(self, agent_vendor_id: str) -> ProxyResponse:
        pass

    async def delete(self, agent_vendor_id: str) -> ProxyResponse:
        pass

    async def create_conversation(
        self,
        agent_vendor_id: str,
        mode_id: str,
        title: str,
        arguments: ContextArguments,
        relation: dict[str, str] | None = None,
    ) -> ProxyResponse:
        pass

    async def get_conversation(self, conversation_id: str) -> ProxyResponse:
        pass

    async def get_conversations(
        self,
        page: int,
        size: int,
        sort_by: str,
        sort_order: str,
        mode: str | None = None,
        title: str | None = None,
        agent_vendor_id: str | None = None,
        document_ids: list[str] | None = None,
    ) -> ProxyResponse:
        pass

    async def get_conversation_completions(self, conversation_id: str, page: int, per_page: int) -> ProxyResponse:
        pass

    async def update_conversation(self, conversation_id: str, title: str) -> ProxyResponse:
        pass

    async def delete_conversations(self, ids: list[str]) -> ProxyResponse:
        pass

    async def get_modes(self) -> ProxyResponse:
        pass
