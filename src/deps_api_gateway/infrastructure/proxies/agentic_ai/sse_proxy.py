import json
import logging
from typing import Any, AsyncGenerator

import httpx

from deps_api_gateway.application import ContextArguments, IAgenticAISSEProxy
from deps_api_gateway.constants import AGENTIC_AI_BASE_API_PREFIX, V1_PREFIX
from deps_api_gateway.domain.exceptions import AuthError

from ...access_management import user
from .exceptions import AgenticAIServiceUnavailableError

__all__ = ["AgenticAISSEProxy"]

SSE_STREAM_TIMEOUT_SECONDS = 600


class AgenticAISSEProxy(IAgenticAISSEProxy):
    v1_prefix = f"{AGENTIC_AI_BASE_API_PREFIX}{V1_PREFIX}"
    conversation_url = f"{v1_prefix}/conversations"

    exception = AgenticAIServiceUnavailableError

    def __init__(
        self,
        base_url: str,
        timeout: int = SSE_STREAM_TIMEOUT_SECONDS,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = httpx.Timeout(timeout)

        self._logger = logging.getLogger(self.__class__.__name__)

    async def chat(
        self,
        conversation_id: str,
        user_question: str,
        arguments: ContextArguments | None = None,
    ) -> AsyncGenerator[bytes, None]:
        url = f"{self._base_url}{self.conversation_url}/{conversation_id}/chat"
        params: dict[str, Any] = {"userQuestion": user_question}

        if arguments is not None:
            params["arguments"] = json.dumps(arguments)

        headers = self._build_headers()

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream("GET", url, params=params, headers=headers) as response:
                await self._check_response(response)

                async for chunk in response.aiter_bytes():
                    yield chunk

    async def edit_question(
        self,
        conversation_id: str,
        completion_id: str,
        user_question: str,
        arguments: ContextArguments | None = None,
    ) -> AsyncGenerator[bytes, None]:
        url = f"{self._base_url}{self.conversation_url}/{conversation_id}/completions/{completion_id}"
        params: dict[str, Any] = {"userQuestion": user_question}

        if arguments is not None:
            params["arguments"] = json.dumps(arguments)

        headers = self._build_headers()

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream("PATCH", url, params=params, headers=headers) as response:
                await self._check_response(response)

                async for chunk in response.aiter_bytes():
                    yield chunk

    async def _check_response(self, response: httpx.Response) -> None:
        if not response.is_success:
            await response.aread()
            self._logger.error(
                "Response to %s failed with status %s and error %s",
                str(response.url),
                response.status_code,
                response.text,
            )
            raise self.exception(response.text)

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",
        }
        user_context = user.get(None)
        if user_context:
            headers["deps-token"] = json.dumps(user_context)
            return headers

        raise AuthError("User context must be provided")
