from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IDocumentType
from deps_api_gateway.constants import (
    DOCUMENT_TYPE_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from deps_api_gateway.domain.exceptions import DocumentTypeError

from ..generic_rest_client import GenericRestClient

__all__ = ["DocumentTypeProxyV1"]


class DocumentTypeProxyV1(GenericRestClient, IDocumentType):
    exception = DocumentTypeError
    v1_prefix = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V2_PREFIX}"

    async def update_document_type_llm(self, type_id: str, llm_data: dict[str, Any]) -> dict[str, Any]:
        try:
            return await self.request(
                method=Methods.PUT,
                url=f"{self.v1_prefix}/types/{type_id}/llm",
                json=llm_data,
            )
        except Exception as error:
            raise self.exception(error)

    async def get_document_types(self) -> dict[str, Any]:
        try:
            return await self.request(method=Methods.GET, url=f"{self.v2_prefix}/types")
        except Exception as error:
            raise self.exception(error)

    async def get_document_type(self, document_type_id: str) -> dict[str, Any]:
        try:
            return await self.request(method=Methods.GET, url=f"{self.v1_prefix}/types/{document_type_id}")
        except Exception as error:
            raise self.exception(error)
