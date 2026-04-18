import asyncio
from typing import Any, Optional

from async_rest_client import Methods
from cachetools import TTLCache

from deps_api_gateway.api.utilities import (
    DocumentType,
    DocumentTypeAggregatedResponse,
    DocumentTypeRoutedResponse,
)
from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    V1_PREFIX,
    DocumentTypeSource,
    ExtractionType,
)

from ..corleone_proxy import ICorleone
from ..document_type_old_proxy import IDocumentTypeOld

__all__ = ["DocumentTypeOldService"]


class _Endpoints:
    def __init__(self) -> None:
        self._document_type_base_path = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}"
        self._corleone_base_path = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}"

    @property
    def corleone_types(self) -> str:
        return f"{self._corleone_base_path}/types"

    @property
    def document_type_types(self) -> str:
        return f"{self._document_type_base_path}/types"

    def corleone_type(self, type_id: str) -> str:
        return f"{self._corleone_base_path}/types/{type_id}"

    def document_type_type(self, type_id: str) -> str:
        return f"{self._document_type_base_path}/types/{type_id}"


class DocumentTypeOldService:
    def __init__(
        self,
        corleone_proxy: ICorleone,
        document_type_proxy: IDocumentTypeOld,
        document_type_source_cache: TTLCache,
    ) -> None:
        self._corleone_proxy = corleone_proxy
        self._document_type_proxy = document_type_proxy
        self._document_type_source_cache = document_type_source_cache

        self._endpoints = _Endpoints()

    async def get_document_types(
        self, deps_token: str, extraction_type: Optional[ExtractionType] = None
    ) -> list[dict[str, Any]]:
        query_corleone = (
            f"extractionType={extraction_type.to_corleone()}"
            if extraction_type and extraction_type != extraction_type.NON
            else ""
        )
        corleone_task = asyncio.create_task(
            self._corleone_proxy.get_document_types(
                method=Methods.GET,
                url=self._endpoints.corleone_types,
                query=query_corleone,
                headers={"deps-token": deps_token},
                data=b"",
            )
        )
        document_type_task = asyncio.create_task(
            self._document_type_proxy.get_document_types(
                method=Methods.GET,
                url=self._endpoints.document_type_types,
                query=f"extractionType={extraction_type.value}" if extraction_type else "",
                headers={"deps-token": deps_token},
                data=b"",
            )
        )

        corleone_resp, document_type_resp = await asyncio.gather(
            corleone_task, document_type_task, return_exceptions=True
        )
        response_content = DocumentTypeAggregatedResponse(corleone_resp, document_type_resp)  # type: ignore
        asyncio.create_task(self._cache_types(response_content))
        return response_content.all_plugins

    async def get_document_type(self, type_id: str, deps_token: str) -> dict[str, Any]:
        source = self._get_type_source(type_id)

        corleone_task = self._corleone_proxy.get_document_type(
            method=Methods.GET,
            url=self._endpoints.corleone_type(type_id),
            query="",
            headers={"deps-token": deps_token},
            data=b"",
        )
        document_type_task = self._document_type_proxy.get_document_type(
            method=Methods.GET,
            url=self._endpoints.document_type_type(type_id),
            query="",
            headers={"deps-token": deps_token},
            data=b"",
        )
        if source == DocumentTypeSource.CORLEONE:
            response_content = DocumentTypeRoutedResponse(corleone_task_result=await corleone_task)
        elif source == DocumentTypeSource.DOCUMENT_TYPE:
            response_content = DocumentTypeRoutedResponse(document_type_task_result=await document_type_task)
        else:
            corleone_task_result, document_type_task_result = await asyncio.gather(
                asyncio.create_task(corleone_task),
                asyncio.create_task(document_type_task),
                return_exceptions=True,
            )
            response_content = DocumentTypeRoutedResponse(corleone_task_result, document_type_task_result)

        self._cache_type(response_content)
        return response_content.chosen_plugin

    async def _cache_types(self, response: DocumentTypeAggregatedResponse) -> None:
        self._update_type_cache(response.corleone, DocumentTypeSource.CORLEONE)
        self._update_type_cache(response.document_type, DocumentTypeSource.DOCUMENT_TYPE)

    def _cache_type(self, response: DocumentTypeRoutedResponse) -> None:
        if response.corleone:
            self._update_type_cache([response.corleone], DocumentTypeSource.CORLEONE)

        if response.document_type:
            self._update_type_cache([response.document_type], DocumentTypeSource.DOCUMENT_TYPE)

    def _update_type_cache(self, types: list[DocumentType], source: DocumentTypeSource) -> None:
        for document_type in types:
            self._document_type_source_cache[document_type.code] = source

    def _get_type_source(self, type_code: str) -> Optional[DocumentTypeSource]:
        return self._document_type_source_cache.get(type_code)

    @staticmethod
    def _get_last_part_of_url(url: str) -> str:
        return url.split("/")[-1]
