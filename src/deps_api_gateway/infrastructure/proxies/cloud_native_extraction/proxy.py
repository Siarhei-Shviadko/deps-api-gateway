from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    ICloudNativeExtractionProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import CLOUD_NATIVE_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import CloudNativeExtractionServiceUnavailableError

__all__ = ["CloudNativeExtractionProxy"]


class CloudNativeExtractionProxy(GenericRestClient, ICloudNativeExtractionProxy):
    exception = CloudNativeExtractionServiceUnavailableError
    v1_prefix = f"{CLOUD_NATIVE_BASE_API_PREFIX}{V1_PREFIX}"

    async def create_azure_extractor(
        self,
        name: str,
        model_id: str,
        endpoint: str,
        api_key: str,
        language: Optional[str],
        description: Optional[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/azure/extractor"

        data: dict[str, Optional[str]] = {
            "name": name,
            "modelId": model_id,
            "endpoint": endpoint,
            "apiKey": api_key,
            "language": language,
            "description": description,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def get_azure_extractor_info(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/azure/extractor/{document_type_id}"

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def validate_credentials(self, model_id: str, endpoint: str, api_key: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/azure/validate-credentials"
        data: dict[str, str] = {
            "modelId": model_id,
            "endpoint": endpoint,
            "apiKey": api_key,
        }
        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_azure_extractor(
        self,
        extractor_id: str,
        model_id: str,
        endpoint: str,
        api_key: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/azure/extractor/{extractor_id}"

        data = {
            "modelId": model_id,
            "endpoint": endpoint,
            "apiKey": api_key,
        }

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))

    async def azure_extractor_checkup(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/azure/extractor/{document_type_id}/checkup"

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def synchronize_azure_extractor(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/azure/extractor/{document_type_id}/synchronize"

        async with self._handling_exception(self.exception):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url))
