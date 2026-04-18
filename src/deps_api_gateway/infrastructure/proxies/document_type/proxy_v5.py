from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IDocumentTypeProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import (
    DOCUMENT_TYPE_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
    ExtractionType,
)

from ..generic_rest_client import GenericRestClient
from .exceptions import DocumentTypeError, DocumentTypeServiceUnavailableError

__all__ = ["DocumentTypeProxyV5"]


class DocumentTypeProxyV5(GenericRestClient, IDocumentTypeProxy):
    exception = DocumentTypeError
    v1_prefix = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V2_PREFIX}"

    async def get_document_types(self, extraction_type: Optional[ExtractionType]) -> ProxyResponse:
        url = f"{self.v2_prefix}/types"

        data = {"extractionType": extraction_type.value} if extraction_type is not None else None

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url, params=data))
        except Exception as error:
            raise DocumentTypeServiceUnavailableError(error)

    async def get_document_type(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/types/{document_type_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise DocumentTypeServiceUnavailableError(error)

    async def delete_document_type(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/types/{document_type_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))
        except Exception as error:
            raise DocumentTypeServiceUnavailableError(error)

    async def update_document_type_llm(self, document_type_id: str, llm_type: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/types/{document_type_id}/llm"
        data = {"llmType": llm_type}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))
