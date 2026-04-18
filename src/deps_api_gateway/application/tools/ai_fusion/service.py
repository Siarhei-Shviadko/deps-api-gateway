from ...iproxies import IAIFusionProxy
from ...proxy_response import ProxyResponse

__all__ = ["AIFusionService"]


class AIFusionService:
    def __init__(
        self,
        ai_fusion_proxy: IAIFusionProxy,
    ) -> None:
        self._ai_fusion_proxy = ai_fusion_proxy

    async def get_llms(self) -> ProxyResponse:
        return await self._ai_fusion_proxy.get_available_models()
