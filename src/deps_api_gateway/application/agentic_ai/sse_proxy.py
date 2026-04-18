from typing import AsyncGenerator, Protocol

from ..types import ContextArguments

__all__ = ["IAgenticAISSEProxy"]


class IAgenticAISSEProxy(Protocol):
    def chat(
        self,
        conversation_id: str,
        user_question: str,
        arguments: ContextArguments | None = None,
    ) -> AsyncGenerator[bytes, None]:
        ...

    async def edit_question(
        self,
        conversation_id: str,
        completion_id: str,
        user_question: str,
        arguments: ContextArguments | None = None,
    ) -> AsyncGenerator[bytes, None]:
        ...
