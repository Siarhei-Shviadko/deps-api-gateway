from typing import Any, Protocol

from async_rest_client import Methods

__all__ = ["ICorleone"]


class ICorleone(Protocol):
    async def get_document_types(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def get_document_type(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def get_extracted_data(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def get_field_chunk(
        self,
        method: Methods,
        url: str,
        query: str,
        headers: dict[str, Any],
        data: bytes,
    ) -> dict:
        ...

    async def delete_extracted_fields(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def put_extracted_data_field(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def update_extracted_data(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def update_extracted_data_cells(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        ...

    async def request(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        ...
