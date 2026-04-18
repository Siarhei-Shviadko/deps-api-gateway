from async_rest_client import Methods

from deps_api_gateway.application import (
    ISemanticParsingProxy,
    Provider,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import SEMANTIC_PARSING_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import ParsingProxyRequestError, ParsingServiceUnavailableError

__all__ = ["SemanticParsingProxy"]


class SemanticParsingProxy(GenericRestClient, ISemanticParsingProxy):
    v1_prefix = f"{SEMANTIC_PARSING_BASE_API_PREFIX}{V1_PREFIX}"
    exception = ParsingProxyRequestError

    async def get_semantic_layout(
        self,
        layout_id: str,
        provider: Provider,
    ) -> ProxyResponse:
        async with self._handling_exception(ParsingServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v1_prefix}/semantic-layout/{layout_id}",
                    params={"provider": provider.value},
                )
            )
