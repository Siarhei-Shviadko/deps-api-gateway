from typing import AsyncGenerator

from ..proxy_response import ProxyResponse
from ..types import ContextArguments
from .proxy import IAgenticAIProxy
from .sse_proxy import IAgenticAISSEProxy

__all__ = ["AgenticAIService"]


class AgenticAIService:
    def __init__(
        self,
        agentic_ai_proxy: IAgenticAIProxy,
        agentic_ai_sse_proxy: IAgenticAISSEProxy,
    ) -> None:
        self._agentic_ai_proxy = agentic_ai_proxy
        self._agentic_ai_sse_proxy = agentic_ai_sse_proxy

    async def create_agent_vendor(
        self,
        name: str,
        description: str,
        base_url: str,
        avatar_url: str | None = None,
    ) -> ProxyResponse:
        return await self._agentic_ai_proxy.create_agent_vendor(
            name=name,
            description=description,
            base_url=base_url,
            avatar_url=avatar_url,
        )

    async def get_agent_vendors(
        self,
    ) -> ProxyResponse:
        return await self._agentic_ai_proxy.get_agent_vendors()

    async def activate(self, agent_vendor_id: str) -> ProxyResponse:
        return await self._agentic_ai_proxy.activate(agent_vendor_id)

    async def create_conversation(
        self,
        agent_vendor_id: str,
        mode_id: str,
        title: str,
        arguments: ContextArguments,
        relation: dict[str, str] | None = None,
    ) -> ProxyResponse:
        return await self._agentic_ai_proxy.create_conversation(
            agent_vendor_id=agent_vendor_id,
            mode_id=mode_id,
            title=title,
            arguments=arguments,
            relation=relation,
        )

    async def delete(self, agent_vendor_id: str) -> ProxyResponse:
        return await self._agentic_ai_proxy.delete(agent_vendor_id)

    async def get_conversation(self, conversation_id: str) -> ProxyResponse:
        return await self._agentic_ai_proxy.get_conversation(conversation_id)

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
        return await self._agentic_ai_proxy.get_conversations(
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order,
            mode=mode,
            title=title,
            agent_vendor_id=agent_vendor_id,
            document_ids=document_ids,
        )

    async def get_completions(self, conversation_id: str, page: int, per_page: int) -> ProxyResponse:
        return await self._agentic_ai_proxy.get_conversation_completions(
            conversation_id=conversation_id, page=page, per_page=per_page
        )

    async def update_conversation(self, conversation_id: str, title: str) -> ProxyResponse:
        return await self._agentic_ai_proxy.update_conversation(conversation_id=conversation_id, title=title)

    async def delete_conversations(self, ids: list[str]) -> ProxyResponse:
        return await self._agentic_ai_proxy.delete_conversations(ids=ids)

    async def get_modes(self) -> ProxyResponse:
        return await self._agentic_ai_proxy.get_modes()

    def chat(
        self,
        conversation_id: str,
        user_question: str,
        arguments: ContextArguments | None = None,
    ) -> AsyncGenerator[bytes, None]:
        return self._agentic_ai_sse_proxy.chat(
            conversation_id=conversation_id,
            user_question=user_question,
            arguments=arguments,
        )

    def edit_question(
        self,
        conversation_id: str,
        completion_id: str,
        user_question: str,
        arguments: ContextArguments | None = None,
    ):
        return self._agentic_ai_sse_proxy.edit_question(
            conversation_id=conversation_id,
            completion_id=completion_id,
            user_question=user_question,
            arguments=arguments,
        )
