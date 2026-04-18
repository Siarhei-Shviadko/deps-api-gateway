from typing import Any, Protocol

from async_rest_client import Methods

__all__ = ["IOCR"]


class IOCR(Protocol):
    async def get_languages(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        ...

    async def get_engines(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> list[dict[str, str]]:
        ...
