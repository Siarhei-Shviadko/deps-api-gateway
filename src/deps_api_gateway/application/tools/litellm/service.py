from ...proxy_response import ProxyResponse
from .proxy import ILiteLLMProxy

__all__ = ["LiteLLMService"]


class LiteLLMService:
    def __init__(self, litellm_proxy: ILiteLLMProxy) -> None:
        self._litellm_proxy = litellm_proxy

    async def get_models(self) -> ProxyResponse:
        return await self._litellm_proxy.get_models()
