import asyncio
from typing import Any, Optional

from deps_api_gateway.api.utilities import DocumentTypeResponse, DocumentTypesResponse

from ...iproxies import IExtraction
from ...proxy_response import ProxyResponse
from ...types import ExtractorType
from ..document_type_proxy import IDocumentType

__all__ = ["DocumentTypeService"]


class DocumentTypeService:
    def __init__(self, document_type_proxy: IDocumentType, extraction_proxy: IExtraction) -> None:
        self._document_type_proxy = document_type_proxy
        self._extraction_proxy = extraction_proxy

    async def update_document_type_llm(self, type_id: str, llm_data: dict[str, Any]) -> dict[str, Any]:
        return await self._document_type_proxy.update_document_type_llm(type_id, llm_data)

    async def create_document_type(self, name: str, description: Optional[str] = None) -> ProxyResponse:
        return await self._extraction_proxy.attach_extractor(
            name=name,
            extractor_type=ExtractorType.NON,
            description=description,
        )

    async def get_document_types(self) -> list[dict[str, Any]]:
        document_type_task = self._document_type_proxy.get_document_types()
        extraction_task = self._extraction_proxy.get_document_types()

        document_type_task_result, extraction_task_result = await asyncio.gather(
            asyncio.create_task(document_type_task),
            asyncio.create_task(extraction_task),
            return_exceptions=True,
        )
        return DocumentTypesResponse(document_type_task_result, extraction_task_result).make_response()  # type: ignore

    async def get_document_type(self, document_type_id: str) -> dict[str, Any]:
        document_type_task = self._document_type_proxy.get_document_type(document_type_id)
        extraction_task = self._extraction_proxy.get_document_type(document_type_id)

        document_type_task_result, extraction_task_result = await asyncio.gather(
            asyncio.create_task(document_type_task),
            asyncio.create_task(extraction_task),
            return_exceptions=True,
        )
        return DocumentTypeResponse(document_type_task_result, extraction_task_result).make_response()  # type: ignore
