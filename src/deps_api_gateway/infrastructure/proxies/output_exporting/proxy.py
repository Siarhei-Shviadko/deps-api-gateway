from async_rest_client import Methods

from deps_api_gateway.application import (
    IOutputExportingProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import OUTPUT_EXPORTING_BASE_PREFIX, V1_PREFIX
from deps_api_gateway.domain import ProfileData

from ..generic_rest_client import GenericRestClient
from .exceptions import OutputExportingError, OutputExportingServiceUnavailableError

__all__ = ["OutputExportingProxy"]


class OutputExportingProxy(GenericRestClient, IOutputExportingProxy):
    v1_prefix = f"{OUTPUT_EXPORTING_BASE_PREFIX}{V1_PREFIX}"
    exception = OutputExportingError

    async def get_outputs(self, document_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document/{document_id}/outputs"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise OutputExportingServiceUnavailableError(error)

    async def get_profiles(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/profiles"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise OutputExportingServiceUnavailableError(error)

    async def save_profile(self, document_type_id: str, profile: ProfileData) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/profiles"
        data = {
            "name": profile.name,
            "schema": profile.schema,
            "format": profile.format,
            "externalStoragesInfo": profile.external_storages_info,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_profile(self, document_type_id: str, profile_id: str, profile: ProfileData) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/profiles/{profile_id}"
        data = {
            "name": profile.name,
            "schema": profile.schema,
            "externalStoragesInfo": profile.external_storages_info,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))

    async def delete_profile(self, document_type_id: str, profile_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/profiles/{profile_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))

    async def build_output(self, document_id: str, document_type_id: str, profile_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document/{document_id}/outputs"
        data = {
            "documentTypeId": document_type_id,
            "profileId": profile_id,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def delete_output(self, document_id: str, output_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document/{document_id}/outputs/{output_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))
