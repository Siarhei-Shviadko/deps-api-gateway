from ..proxy_response import ProxyResponse
from .proxy import IMetaAgentProxy

__all__ = ["MetaAgentService"]


class MetaAgentService:
    def __init__(
        self,
        meta_agent_proxy: IMetaAgentProxy,
    ) -> None:
        self._meta_agent_proxy = meta_agent_proxy

    async def register_manifest(
        self,
        code: str,
        name: str,
        description: str,
        url: str,
        timeout: int,
    ) -> ProxyResponse:
        return await self._meta_agent_proxy.register_manifest(
            code=code,
            name=name,
            description=description,
            url=url,
            timeout=timeout,
        )

    async def delete_manifests(
        self,
        codes: list[str],
    ) -> ProxyResponse:
        return await self._meta_agent_proxy.delete_manifests(
            codes=codes,
        )
