from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application import (
    ContextArguments,
    IAgenticAIProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import AGENTIC_AI_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import AgenticAIServiceUnavailableError

__all__ = ["AgenticAIProxy"]


class AgenticAIProxy(GenericRestClient, IAgenticAIProxy):
    v1_prefix = f"{AGENTIC_AI_BASE_API_PREFIX}{V1_PREFIX}"
    agent_vendor_url = f"{v1_prefix}/agent-vendors"
    conversation_url = f"{v1_prefix}/conversations"
    mode_url = f"{v1_prefix}/modes"

    exception = AgenticAIServiceUnavailableError

    async def create_agent_vendor(
        self,
        name: str,
        description: str,
        base_url: str,
        avatar_url: str | None = None,
    ) -> ProxyResponse:
        data = {
            "name": name,
            "description": description,
            "baseUrl": base_url,
            "avatarUrl": avatar_url,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=self.agent_vendor_url, json=data)
            )

    async def get_agent_vendors(self) -> ProxyResponse:
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=self.agent_vendor_url)
            )

    async def activate(
        self,
        agent_vendor_id: str,
    ) -> ProxyResponse:
        url = f"{self.agent_vendor_url}/{agent_vendor_id}/activate"

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url))

    async def create_conversation(
        self,
        agent_vendor_id: str,
        mode_id: str,
        title: str,
        arguments: ContextArguments,
        relation: dict[str, str] | None = None,
    ) -> ProxyResponse:
        url = f"{self.conversation_url}"

        data = {
            "agentVendorId": agent_vendor_id,
            "modeId": mode_id,
            "title": title,
            "arguments": arguments,
            "relation": relation,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def delete(
        self,
        agent_vendor_id: str,
    ) -> ProxyResponse:
        url = f"{self.agent_vendor_url}/{agent_vendor_id}"

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))

    async def get_conversation(self, conversation_id: str) -> ProxyResponse:
        url = f"{self.conversation_url}/{conversation_id}"
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def get_conversations(
        self,
        page: int,
        size: int,
        sort_by: str,
        sort_order: str,
        mode: str | None = None,
        title: str | None = None,
        agent_vendor_id: str | None = None,
        document_ids: list[str] | None = None,
    ) -> ProxyResponse:
        url = self.conversation_url
        params: dict[str, Any] = {
            "page": page,
            "size": size,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }

        if mode is not None:
            params["mode"] = mode
        if title is not None:
            params["title"] = title
        if agent_vendor_id is not None:
            params["agent_vendor_id"] = agent_vendor_id
        if document_ids:
            params["documentId"] = document_ids

        async with self._handling_exception(self.exception):
            response = await self.request(method=Methods.GET, url=url, params=params)
            return ProxyResponseFactory.make_response_from(response)

    async def get_conversation_completions(self, conversation_id: str, page: int, per_page: int) -> ProxyResponse:
        url = f"{self.conversation_url}/{conversation_id}/completions"
        params = {"page": page, "perPage": per_page}

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=url, params=params)
            )

    async def update_conversation(self, conversation_id: str, title: str) -> ProxyResponse:
        url = f"{self.conversation_url}/{conversation_id}"
        data = {"title": title}

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

    async def delete_conversations(self, ids: list[str]) -> ProxyResponse:
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=self.conversation_url, params={"id": ids})
            )

    async def get_modes(self) -> ProxyResponse:
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=self.mode_url))
