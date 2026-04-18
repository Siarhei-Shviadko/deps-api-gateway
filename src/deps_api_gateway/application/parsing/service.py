from ..proxy_response import ProxyResponse
from .proxy import IParsingProxy

__all__ = ["ParsingService"]


class ParsingService:
    def __init__(
        self,
        parsing_proxy: IParsingProxy,
    ) -> None:
        self._parsing_proxy = parsing_proxy

    async def get_parsing_info(self, document_id: str) -> ProxyResponse:
        return await self._parsing_proxy.get_parsing_info(document_id)

    async def clone_document_layout(self, document_id: str, parsing_type: str) -> ProxyResponse:
        return await self._parsing_proxy.clone_document_layout(document_id=document_id, parsing_type=parsing_type)
