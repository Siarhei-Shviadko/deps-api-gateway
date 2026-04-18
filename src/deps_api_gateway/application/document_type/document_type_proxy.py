from typing import Protocol

from deps_api_gateway.constants import ExtractionType

from ..proxy_response import ProxyResponse

__all__ = ["IDocumentTypeProxy"]


class IDocumentTypeProxy(Protocol):
    async def get_document_types(self, extraction_type: ExtractionType) -> ProxyResponse:
        ...

    async def get_document_type(self, document_type_id: str) -> ProxyResponse:
        ...

    async def delete_document_type(self, document_type_id: str) -> ProxyResponse:
        ...

    async def update_document_type_llm(self, document_type_id: str, llm_type: str) -> ProxyResponse:
        ...
