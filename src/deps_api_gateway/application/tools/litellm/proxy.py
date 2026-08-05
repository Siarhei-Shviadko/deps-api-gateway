from typing import Protocol

from ...proxy_response import ProxyResponse

__all__ = ["ILiteLLMProxy"]


class ILiteLLMProxy(Protocol):
    async def get_models(self) -> ProxyResponse:
        ...
