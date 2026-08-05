from deps_api_gateway.application.parsing import LayoutType
from deps_api_gateway.application.parsing.proxy import IParsingProxy
from deps_api_gateway.application.proxy_response import ProxyResponse

__all__ = ["ParsingToolsService"]


class ParsingToolsService:
    def __init__(self, parsing_proxy: IParsingProxy) -> None:
        self._parsing_proxy = parsing_proxy

    async def get_engines(self, layout_type: LayoutType | None = None) -> ProxyResponse:
        layout_type_value = layout_type.value if layout_type else None
        return await self._parsing_proxy.get_engines(layout_type_value)
