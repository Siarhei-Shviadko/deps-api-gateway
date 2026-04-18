from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IEnrichment
from deps_api_gateway.constants import ENRICHMENT_BASE_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import EnrichmentError

__all__ = ["OldEnrichmentProxy"]


class OldEnrichmentProxy(GenericRestClient, IEnrichment):
    exception = EnrichmentError
    v1_prefix = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}"

    async def create_extra_field(self, document_type_id: str, name: str, display_order: int) -> dict[str, Any]:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"
        data = {
            "name": name,
            "order": display_order,
        }

        try:
            return await self.request(method=Methods.POST, url=url, json=data)
        except Exception as error:
            raise EnrichmentError(error)

    async def delete_extra_fields(self, document_type_id: str, extra_field_codes: list[str]) -> dict[str, Any]:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"
        params = {"extraFieldCodes": extra_field_codes}

        try:
            return await self.request(method=Methods.DELETE, url=url, params=params)
        except Exception as error:
            raise EnrichmentError(error)

    async def get_extra_fields(self, document_type_id: str) -> dict[str, Any]:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"

        try:
            return await self.request(method=Methods.GET, url=url)
        except Exception as error:
            raise EnrichmentError(error)

    async def create_or_modify_supplement(
        self, document_id: str, document_type_id: str, extra_data: list[dict[str, Any]]
    ) -> dict[str, str]:
        url = f"{self.v1_prefix}/supplements/{document_id}"
        data = {"data": extra_data, "documentTypeId": document_type_id}

        try:
            return await self.request(method=Methods.PUT, url=url, json=data)
        except Exception as error:
            raise EnrichmentError(error)

    async def find_supplement(self, document_id: str) -> dict[str, Any]:
        url = f"{self.v1_prefix}/supplements/{document_id}"

        try:
            return await self.request(method=Methods.GET, url=url)
        except Exception as error:
            raise EnrichmentError(error)

    async def update_extra_fields(self, document_type_id: str, extra_fields: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"

        try:
            return await self.request(method=Methods.PUT, url=url, json=extra_fields)
        except Exception as error:
            raise EnrichmentError(error)
