from typing import Any

from async_rest_client import AbstractRestClient, Methods

__all__ = ["OldGenericRestClient"]


class OldGenericRestClient(AbstractRestClient):
    async def request(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        async with self._client.request(
            method=method,
            url=f"{url}?{query}",
            headers=headers,
            data=data,
        ) as response:
            return {
                "content": await response.read(),
                "status_code": response.status,
                "headers": response.headers,
            }
