from typing import Any

from .enrichment_proxy import IEnrichment

__all__ = ["EnrichmentService"]


class EnrichmentService:
    def __init__(self, enrichment_proxy: IEnrichment):
        self._enrichment_proxy = enrichment_proxy

    async def create_extra_field(self, document_type_id: str, name: str, display_order: int) -> dict[str, Any]:
        return await self._enrichment_proxy.create_extra_field(
            document_type_id=document_type_id,
            name=name,
            display_order=display_order,
        )

    async def delete_extra_fields(self, document_type_id: str, extra_field_codes: list[str]) -> dict[str, Any]:
        return await self._enrichment_proxy.delete_extra_fields(document_type_id, extra_field_codes)

    async def get_extra_fields(self, document_type_id: str) -> dict[str, Any]:
        return await self._enrichment_proxy.get_extra_fields(document_type_id)

    async def create_or_modify_supplement(
        self, document_id: str, document_type_id: str, extra_data: list[dict[str, Any]]
    ) -> dict[str, str]:
        return await self._enrichment_proxy.create_or_modify_supplement(document_id, document_type_id, extra_data)

    async def find_supplement(self, document_id: str) -> dict[str, Any]:
        return await self._enrichment_proxy.find_supplement(document_id)

    async def update_extra_fields(self, document_type_id: str, extra_fields: dict[str, Any]) -> dict[str, Any]:
        return await self._enrichment_proxy.update_extra_fields(
            document_type_id=document_type_id, extra_fields=extra_fields
        )
