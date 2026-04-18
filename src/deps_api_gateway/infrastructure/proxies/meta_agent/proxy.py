from async_rest_client import Methods

from deps_api_gateway.application import (
    IMetaAgentProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import META_AGENT_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import MetaAgentServiceUnavailableError

__all__ = ["MetaAgentProxy"]


class MetaAgentProxy(GenericRestClient, IMetaAgentProxy):
    exception = MetaAgentServiceUnavailableError

    v1_prefix = f"{META_AGENT_BASE_API_PREFIX}{V1_PREFIX}"
    agentic_manifest_url = f"{v1_prefix}/manifests"

    async def register_manifest(
        self,
        code: str,
        name: str,
        description: str,
        url: str,
        timeout: int,
    ) -> ProxyResponse:
        payload = {
            "code": code,
            "name": name,
            "description": description,
            "url": url,
            "timeout": timeout,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=self.agentic_manifest_url, json=payload)
            )

    async def delete_manifests(
        self,
        codes: list[str],
    ) -> ProxyResponse:
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=self.agentic_manifest_url, params={"code": codes})
            )
