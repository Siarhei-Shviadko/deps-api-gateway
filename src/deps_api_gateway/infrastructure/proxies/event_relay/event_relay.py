from http import HTTPStatus
from typing import Any, AsyncGenerator, Optional, final

from async_rest_client import CommonDictType, Methods

from deps_api_gateway.constants import EVENT_RELAY_BASE_API_PREFIX, V1_PREFIX

from ....application import IEventRelayProxy
from ..generic_rest_client import GenericRestClient
from .exceptions import EventRelayError

__all__ = ["EventRelayProxy"]


class EventRelayProxy(GenericRestClient, IEventRelayProxy):
    ALLOWED_STATUS_CODES = {HTTPStatus.OK}
    exception = EventRelayError
    v1_prefix = f"{EVENT_RELAY_BASE_API_PREFIX}{V1_PREFIX}"

    def __init__(
        self,
        base_url: str,
        *,
        verify_ssl: bool = False,
        timeout: int = 60,
        headers: Optional[CommonDictType] = None,
    ) -> None:
        timeout_override = 3600
        timeout = max(timeout_override, timeout)
        super().__init__(base_url=base_url, verify_ssl=verify_ssl, timeout=timeout, headers=headers)

    @final
    async def request(self, *, method: Methods, url: str, **kwargs) -> dict[str, Any]:
        raise RuntimeError("You shouldn't use GenericRestClient.request when dealing with SSEs")

    async def subscribe(self) -> AsyncGenerator[bytes, None]:
        url = f"{self.v1_prefix}/stream"
        async for chunk in self._request_sse(url=url, headers={"Connection": "keep-alive"}, method=Methods.GET):
            yield chunk

    async def _request_sse(self, method: Methods, url: str, **kwargs) -> AsyncGenerator[bytes, None]:
        headers = self._unify_headers(kwargs)
        async with self._client.request(url=url, method=method, headers=headers, **kwargs) as response:
            async for chunk in response.content:
                yield chunk
