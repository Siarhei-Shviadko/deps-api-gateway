from async_rest_client import Methods

from deps_api_gateway.application import (
    ILiteLLMProxy,
    ProxyResponse,
    ProxyResponseFactory,
)

from ..generic_rest_client import GenericRestClient
from .exceptions import LiteLLMError, LiteLLMServiceUnavailableError

__all__ = ["LiteLLMProxy"]


class LiteLLMProxy(GenericRestClient, ILiteLLMProxy):
    exception = LiteLLMError

    def __init__(self, base_url: str, api_key: str, *, verify_ssl: bool = False) -> None:
        super().__init__(base_url, verify_ssl=verify_ssl, headers={"Authorization": f"Bearer {api_key}"})

    async def get_models(self) -> ProxyResponse:
        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url="/models"))
        except Exception as error:
            raise LiteLLMServiceUnavailableError(error)
