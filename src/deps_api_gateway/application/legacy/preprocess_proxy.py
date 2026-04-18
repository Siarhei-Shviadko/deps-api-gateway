from typing import Any, Protocol

from async_rest_client import Methods

__all__ = ["IPreprocess"]


class IPreprocess(Protocol):
    async def get_unified_data(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...
