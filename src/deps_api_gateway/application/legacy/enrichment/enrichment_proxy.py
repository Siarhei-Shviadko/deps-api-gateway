from typing import Any, Protocol

__all__ = ["IEnrichment"]


class IEnrichment(Protocol):
    async def create_extra_field(self, document_type_id: str, name: str, display_order: int) -> dict[str, Any]:
        ...

    async def delete_extra_fields(self, document_type_id: str, extra_field_codes: list[str]) -> dict[str, Any]:
        ...

    async def get_extra_fields(self, document_type_id: str) -> dict[str, Any]:
        ...

    async def create_or_modify_supplement(
        self, document_id: str, document_type_id: str, extra_data: list[dict[str, Any]]
    ) -> dict[str, str]:
        ...

    async def find_supplement(self, document_id: str) -> dict[str, Any]:
        ...

    async def update_extra_fields(self, document_type_id: str, extra_fields: dict[str, Any]) -> dict[str, Any]:
        ...
