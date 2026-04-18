from typing import Any, Protocol

__all__ = ["IDocumentType"]


class IDocumentType(Protocol):
    async def get_document_types(self) -> dict[str, Any]:
        ...

    async def get_document_type(self, document_type_id: str) -> dict[str, Any]:
        ...

    async def update_document_type_llm(self, type_id: str, llm_data: dict[str, Any]) -> dict[str, Any]:
        ...
