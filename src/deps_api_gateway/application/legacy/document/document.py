import asyncio
from functools import cached_property

from async_rest_client import Methods
from cachetools import TTLCache

from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    DOCUMENT_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    OCR_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
)
from deps_api_gateway.domain.dtos import DocumentListFilter

from ..corleone_proxy import ICorleone
from ..document_proxy import IDocument
from ..document_type_old_proxy import IDocumentTypeOld
from .aggregate_cacher import DocumentAggregateCacher
from .aggregator import DocumentResponseAggregator
from .cacher import Cacher, CacheTypes, RareCacheKeys
from .ocr_proxy import IOCR
from .validator import DocumentResponseValidator

__all__ = ["DocumentService"]


async def _return_value(value):
    return value


class _Endpoints:
    def __init__(self) -> None:
        self._document_base_path = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}"
        self._corleone_base_path = f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}"
        self._document_types_base_path = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}"
        self._ocr_base_path = f"{OCR_BASE_API_PREFIX}"

    @cached_property
    def document_list(self):
        return f"{self._document_base_path}/documents"

    @cached_property
    def corleone_types(self):
        return f"{self._corleone_base_path}/types"

    @cached_property
    def document_type_types(self):
        return f"{self._document_types_base_path}/types"

    @cached_property
    def ocr_engines(self):
        return f"{self._ocr_base_path}{V2_PREFIX}/engines"

    @cached_property
    def ocr_languages(self):
        return f"{self._ocr_base_path}{V1_PREFIX}/languages"

    @cached_property
    def document_states(self):
        return f"{self._document_base_path}/documents/states"


class DocumentService:
    def __init__(
        self,
        document_proxy: IDocument,
        corleone_proxy: ICorleone,
        document_type_proxy: IDocumentTypeOld,
        ocr_proxy: IOCR,
        rarely_updatable_cache: TTLCache,
        document_type_source_cache: TTLCache,
        document_type_code_cache: TTLCache,
        document_type_extraction_type_cache: TTLCache,
    ):
        self._document_proxy = document_proxy
        self._corleone_proxy = corleone_proxy
        self._document_type_proxy = document_type_proxy
        self._ocr_proxy = ocr_proxy
        self._cacher: Cacher = Cacher(
            rare_cache=rarely_updatable_cache,
            doc_type_code_cache=document_type_code_cache,
            doc_type_source_cache=document_type_source_cache,
            doc_type_extraction_cache=document_type_extraction_type_cache,
        )
        self._endpoints = _Endpoints()

    async def get_documents(self, filter_: DocumentListFilter, deps_token: str) -> dict:
        (
            document_list_response,
            corleone_types_response,
            document_type_types_response,
            engines_response,
            languages_response,
            states_response,
            *_,
        ) = await asyncio.gather(
            await self._get_docs_list_task(deps_token, filter_.raw_query),
            await self._get_corleone_document_types_task(deps_token),
            await self._get_document_types_task(deps_token),
            await self._get_ocr_engines_task(deps_token),
            await self._get_ocr_languages(deps_token),
            await self._get_document_states_task(deps_token),
            return_exceptions=True,
        )
        (
            DocumentResponseValidator()
            .for_document(document_list_response)
            .with_corleone_types(corleone_types_response)
            .with_document_type_types(document_type_types_response)
            .with_engines(engines_response)
            .with_languages(languages_response)
            .with_states(states_response)
            .validate()
        )

        aggregator = (
            DocumentResponseAggregator()
            .for_document(document_list_response)
            .with_corleone_types(corleone_types_response)
            .with_document_type_types(document_type_types_response)
            .with_engines(engines_response)
            .with_languages(languages_response)
            .with_states(states_response)
        )
        aggregated = aggregator.aggregate()

        cache_tasks = (
            DocumentAggregateCacher(self._cacher)  # noqa: WPS221
            .with_document_type_types(aggregator.document_type_types)
            .with_states(aggregator.document_states)
            .with_corleone_types(aggregator.corleone_types)
            .with_engines(aggregator.ocr_engines)
            .with_languages(aggregator.ocr_languages)
            .for_documents(aggregator.documents)
            .with_aggregator_response(aggregated)
        )
        asyncio.create_task(cache_tasks.cache())
        return aggregated  # type: ignore

    async def _get_ocr_languages(self, deps_token):
        if from_cache := await self._cacher.get(CacheTypes.RARE, RareCacheKeys.LANGUAGES.value):
            return asyncio.create_task(_return_value(from_cache))
        return asyncio.create_task(
            self._ocr_proxy.get_languages(
                method=Methods.GET,
                url=self._endpoints.ocr_languages,
                query="",
                headers={"deps-token": deps_token},
                data=b"",
            )
        )

    async def _get_ocr_engines_task(self, deps_token):
        if from_cache := await self._cacher.get(CacheTypes.RARE, RareCacheKeys.ENGINES.value):
            return asyncio.create_task(_return_value(from_cache))
        return asyncio.create_task(
            self._ocr_proxy.get_engines(
                method=Methods.GET,
                url=self._endpoints.ocr_engines,
                query="",
                headers={"deps-token": deps_token},
                data=b"",
            )
        )

    async def _get_document_types_task(self, deps_token: str):
        return asyncio.create_task(
            self._document_type_proxy.get_document_types(
                url=self._endpoints.document_type_types,
                method=Methods.GET,
                query="",
                headers={"deps-token": deps_token},
                data=b"",
            )
        )

    async def _get_corleone_document_types_task(self, deps_token):
        return self._corleone_proxy.get_document_types(
            url=self._endpoints.corleone_types,
            method=Methods.GET,
            query="",
            headers={"deps-token": deps_token},
            data=b"",
        )

    async def _get_document_states_task(self, deps_token):
        if from_cache := await self._cacher.get(CacheTypes.RARE, RareCacheKeys.STATES.value):
            return asyncio.create_task(_return_value(from_cache))
        return asyncio.create_task(
            self._document_proxy.get_states(
                method=Methods.GET,
                url=self._endpoints.document_states,
                headers={"deps-token": deps_token},
                data=b"",
                query="",
            )
        )

    async def _get_docs_list_task(self, deps_token: str, query_filter: str):
        return asyncio.create_task(
            self._document_proxy.list_documents(
                method=Methods.GET,
                url=self._endpoints.document_list,
                headers={"deps-token": deps_token},
                query=query_filter,
                data=b"",
            )
        )
