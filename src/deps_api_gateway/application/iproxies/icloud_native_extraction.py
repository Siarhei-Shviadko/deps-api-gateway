from typing import Optional, Protocol

from ..proxy_response import ProxyResponse

__all__ = ["ICloudNativeExtractionProxy"]


class ICloudNativeExtractionProxy(Protocol):
    async def create_azure_extractor(
        self,
        name: str,
        model_id: str,
        endpoint: str,
        api_key: str,
        language: Optional[str],
        description: Optional[str],
    ) -> ProxyResponse:
        ...

    async def get_azure_extractor_info(
        self,
        document_type_id: str,
    ) -> ProxyResponse:
        ...

    async def validate_credentials(
        self,
        model_id: str,
        endpoint: str,
        api_key: str,
    ) -> ProxyResponse:
        ...

    async def update_azure_extractor(
        self,
        extractor_id: str,
        model_id: str,
        endpoint: str,
        api_key: str,
    ) -> ProxyResponse:
        ...

    async def azure_extractor_checkup(
        self,
        document_type_id: str,
    ) -> ProxyResponse:
        ...

    async def synchronize_azure_extractor(
        self,
        document_type_id: str,
    ) -> ProxyResponse:
        ...
