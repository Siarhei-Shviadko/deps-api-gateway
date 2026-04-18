from typing import Any, Protocol

from async_rest_client import Methods

__all__ = ["IDocumentTypeOld"]


class IDocumentTypeOld(Protocol):
    async def get_document_types(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def get_document_type(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...
