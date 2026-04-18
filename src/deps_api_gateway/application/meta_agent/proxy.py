from typing import Protocol

from ..proxy_response import ProxyResponse

__all__ = ["IMetaAgentProxy"]


class IMetaAgentProxy(Protocol):
    async def register_manifest(
        self,
        code: str,
        name: str,
        description: str,
        url: str,
        timeout: int,
    ) -> ProxyResponse:
        pass

    async def delete_manifests(
        self,
        codes: list[str],
    ) -> ProxyResponse:
        pass
