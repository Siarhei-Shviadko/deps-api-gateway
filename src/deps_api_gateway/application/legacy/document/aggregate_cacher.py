import asyncio
from typing import Optional

from deps_api_gateway.constants import DocumentTypeSource

from .cacher import Cacher, CacheTypes, RareCacheKeys
from .is_exception import is_exception
from .typehints import (
    AggregatedDocumentList,
    CodeName,
    CorleoneResponse,
    DocumentListProxyResponse,
    DocumentTypeResponse,
    States,
)

__all__ = ["DocumentAggregateCacher"]


class DocumentAggregateCacher:
    def __init__(self, cacher: Cacher) -> None:
        self._documents: Optional[DocumentListProxyResponse] = None
        self._corleone_types: Optional[CorleoneResponse] = None
        self._document_type_types: Optional[list[DocumentTypeResponse]] = None
        self._ocr_engines: Optional[list[CodeName]] = None
        self._ocr_languages: Optional[list[CodeName]] = None
        self._document_states: Optional[States] = None
        self._aggregated: Optional[AggregatedDocumentList] = None
        self._cacher = cacher

    def for_documents(self, document_list: DocumentListProxyResponse) -> "DocumentAggregateCacher":
        self._documents = document_list
        return self

    def with_corleone_types(self, corleone_types: CorleoneResponse) -> "DocumentAggregateCacher":
        self._corleone_types = corleone_types
        return self

    def with_document_type_types(self, document_type_types: list[DocumentTypeResponse]) -> "DocumentAggregateCacher":
        self._document_type_types = document_type_types
        return self

    def with_engines(self, ocr_engines: list[CodeName]) -> "DocumentAggregateCacher":
        self._ocr_engines = ocr_engines
        return self

    def with_languages(self, ocr_languages: list[CodeName]) -> "DocumentAggregateCacher":
        self._ocr_languages = ocr_languages
        return self

    def with_states(self, document_states: States) -> "DocumentAggregateCacher":
        self._document_states = document_states
        return self

    def with_aggregator_response(self, aggregated: AggregatedDocumentList) -> "DocumentAggregateCacher":
        self._aggregated = aggregated
        return self

    async def cache(self):
        asyncio.create_task(self._cache_rare_cases())
        asyncio.create_task(self._cache_document_type_code_cache())
        asyncio.create_task(self._update_corleone_caches())
        asyncio.create_task(self._update_doc_type_service_caches())

    async def _cache_rare_cases(self):
        await self._cacher.cache(CacheTypes.RARE, RareCacheKeys.STATES.value, self._document_states)
        await self._cacher.cache(CacheTypes.RARE, RareCacheKeys.ENGINES.value, self._ocr_engines)
        await self._cacher.cache(CacheTypes.RARE, RareCacheKeys.LANGUAGES.value, self._ocr_languages)

    async def _update_corleone_caches(self):
        if self._corleone_types and not is_exception(self._corleone_types):
            for type_ in self._corleone_types["result"]:
                doc_type_code = type_["code"]
                extraction_type = type_["extractionType"]
                await self._cacher.cache(CacheTypes.DOC_TYPE_SOURCE, doc_type_code, DocumentTypeSource.CORLEONE)
                await self._cacher.cache(CacheTypes.DOC_TYPE_EXTRACTION, doc_type_code, extraction_type)

    async def _update_doc_type_service_caches(self):
        if self._document_type_types and not is_exception(self._document_type_types):
            for type_ in self._document_type_types:
                doc_type_code = type_["id"]
                extraction_type = type_["extractionType"]
                await self._cacher.cache(CacheTypes.DOC_TYPE_SOURCE, doc_type_code, DocumentTypeSource.DOCUMENT_TYPE)
                await self._cacher.cache(CacheTypes.DOC_TYPE_EXTRACTION, doc_type_code, extraction_type)

    async def _cache_document_type_code_cache(self):
        if self._aggregated:
            for doc in self._aggregated["result"]:
                if doc["documentType"]:
                    await self._cacher.cache(CacheTypes.DOC_TYPE_CODE, doc["id"], doc["documentType"]["code"])
