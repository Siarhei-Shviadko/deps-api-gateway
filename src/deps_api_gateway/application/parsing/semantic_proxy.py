from typing import Protocol

from ..proxy_response import ProxyResponse
from .provider import Provider

__all__ = ["ISemanticParsingProxy"]


class ISemanticParsingProxy(Protocol):
    async def get_semantic_layout(
        self,
        layout_id: str,
        provider: Provider,
    ) -> ProxyResponse:
        ...
