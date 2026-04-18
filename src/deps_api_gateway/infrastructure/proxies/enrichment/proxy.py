from async_rest_client import Methods

from deps_api_gateway.application import (
    IEnrichmentProxy,
    ProxyResponse,
    ProxyResponseFactory,
    SaveExtraDataElement,
)
from deps_api_gateway.constants import ENRICHMENT_BASE_PREFIX, V1_PREFIX
from deps_api_gateway.domain import ExtraFieldData

from ..generic_rest_client import GenericRestClient
from .exceptions import EnrichmentError, EnrichmentServiceUnavailableError

__all__ = ["EnrichmentProxy"]


class EnrichmentProxy(GenericRestClient, IEnrichmentProxy):
    exception = EnrichmentError
    v1_prefix = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}"

    async def get_extra_fields(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise EnrichmentServiceUnavailableError(error)

    async def get_document_supplement(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/supplements/{document_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise EnrichmentServiceUnavailableError(error)

    async def save_document_supplement(
        self,
        document_id: str,
        document_type_id: str,
        extra_data_list: list[SaveExtraDataElement],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/supplements/{document_id}"
        data = {"documentTypeId": document_type_id, "data": extra_data_list}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))

    async def save_extra_fields(self, document_type_id: str, name: str, order: int) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"
        data = {"name": name, "order": order}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_extra_fields(self, document_type_id: str, fields: list[ExtraFieldData]) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"

        data = {
            "extraFields": [
                {
                    "code": field.code,
                    "name": field.name,
                    "order": field.display_order,
                }
                for field in fields
            ]
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))

    async def delete_extra_fields(self, document_type_id: str, extra_field_codes: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/extra-fields"
        data = {"extraFieldCodes": extra_field_codes}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params=data),
            )
