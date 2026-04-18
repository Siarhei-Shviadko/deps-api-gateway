import asyncio
import re
from typing import Optional

from async_rest_client import Methods
from cachetools import TTLCache
from fastapi.responses import Response

from deps_api_gateway.api.utilities import (
    ExtractedDataRoutedResponse,
    ParsedRequest,
    ResponseBuilder,
    TypeContent,
    TypeRoutedResponse,
    TypesAggregatedResponse,
)
from deps_api_gateway.application.legacy import ICorleone, IDocumentType, IExtractionOld
from deps_api_gateway.constants import (
    CORLEONE_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
    DocumentTypeSource,
    ExtractedDataSource,
)
from deps_api_gateway.infrastructure import OldGenericRestClient

from .abstract_router import AbstractRouter, RequestMapper

__all__ = ["CorleoneRouter"]


class CorleoneRouter(AbstractRouter):
    def __init__(
        self,
        client: OldGenericRestClient,
        corleone_proxy: ICorleone,
        document_type_proxy: IDocumentType,
        extraction_proxy: IExtractionOld,
        document_type_source_cache: TTLCache,
        document_type_code_cache: TTLCache,
        document_type_extraction_type_cache: TTLCache,
    ) -> None:
        super().__init__(client)
        self._corleone_proxy = corleone_proxy
        self._document_type_proxy = document_type_proxy
        self._extraction_proxy = extraction_proxy
        self._document_type_source_cache = document_type_source_cache
        self._document_type_code_cache = document_type_code_cache
        self._document_type_extraction_type_cache = document_type_extraction_type_cache

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (Methods.GET, rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/types/\w+$"): self._get_document_type,
            (Methods.GET, f"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/types$"): self._get_document_types,
            (Methods.GET, rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/\d+$"): self._get_extracted_data,
            (
                Methods.DELETE,
                rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/\d+/fields$",
            ): self._delete_extracted_data_fields,
            (
                Methods.PUT,
                rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/\d+/field$",
            ): self._put_extracted_data_field,
            (Methods.PUT, rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/\d+$"): self._update_extracted_data,
            (
                Methods.GET,
                rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/\d+/fields/\w+/chunk$",
            ): self._get_field_chunk,
            (Methods.PUT, f"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/plugins/register$"): self._register_corleone_plugin,
            (
                Methods.PATCH,
                rf"^{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}/extracted-data/\d+/fields/\w+$",
            ): self._update_extracted_data_cells,
        }

    async def _get_field_chunk(self, request: ParsedRequest) -> Response:
        document_id = self._get_document_id_from_extracted_data_url(request.url)
        extracted_data_source = self._get_extracted_data_source(document_id)

        routed_response = await self._route_get_field_chunk_request(request, extracted_data_source)
        return (
            ResponseBuilder()
            .with_status(routed_response.status_code)
            .with_content(routed_response.chosen_extracted_data_json)
            .build()
        )

    async def _get_document_types(self, request: ParsedRequest) -> Response:
        corleone_service_task = asyncio.create_task(self._corleone_proxy.get_document_types(**await request.to_dict()))

        type_service_task = asyncio.create_task(
            self._document_type_proxy.get_document_types(
                **await request.change_url(CORLEONE_BASE_API_PREFIX, DOCUMENT_TYPE_BASE_API_PREFIX).to_dict(),  # type: ignore
            )
        )

        finished_tasks = await asyncio.gather(corleone_service_task, type_service_task, return_exceptions=True)

        aggregated_response = TypesAggregatedResponse(finished_tasks)

        asyncio.create_task(self._cache_types(aggregated_response))
        return ResponseBuilder().with_content(aggregated_response.all_types_json).build()

    async def _get_document_type(self, request: ParsedRequest) -> Response:
        type_code = self._get_type_code_from_type_url(request.url)
        type_source = self._get_type_source(type_code)

        routed_response = await self._route_get_type_request(
            request,
            type_source,
        )

        self._cache_type(routed_response)

        return ResponseBuilder().with_content(routed_response.chosen_type_json).build()

    async def _get_extracted_data(self, request: ParsedRequest) -> Response:
        document_id = self._get_document_id_from_extracted_data_url(request.url)
        extracted_data_source = self._get_extracted_data_source(document_id)

        routed_response = await self._route_get_edata_request(request, extracted_data_source)

        return (
            ResponseBuilder()
            .with_content(routed_response.chosen_extracted_data_json)
            .with_status(routed_response.status_code)
            .build()
        )

    async def _put_extracted_data_field(self, request: ParsedRequest) -> Response:
        document_id = self._get_document_id_from_extracted_data_url(request.url)
        extracted_data_source = self._get_extracted_data_source(document_id)
        routed_response = await self._route_put_edata_field_request(request, extracted_data_source)
        return ResponseBuilder().with_content(routed_response.chosen_extracted_data_json).build()

    async def _delete_extracted_data_fields(self, request: ParsedRequest) -> Response:
        document_id = self._get_document_id_from_extracted_data_url(request.url)
        extracted_data_source = self._get_extracted_data_source(document_id)

        routed_response = await self._route_delete_edata_fields_request(request, extracted_data_source)
        return ResponseBuilder().with_content(routed_response.chosen_extracted_data_json).build()

    async def _update_extracted_data(self, request: ParsedRequest) -> Response:
        document_id = self._get_document_id_from_extracted_data_url(request.url)
        extracted_data_source = self._get_extracted_data_source(document_id)

        routed_response = await self._route_update_edata_request(request, extracted_data_source)

        return ResponseBuilder().with_content(routed_response.chosen_extracted_data_json).build()

    async def _update_extracted_data_cells(self, request: ParsedRequest) -> Response:
        document_id = self._get_document_id_from_extracted_data_url(request.url)
        extracted_data_source = self._get_extracted_data_source(document_id)

        routed_response = await self._route_update_edata_cells_request(request, extracted_data_source)

        return ResponseBuilder().with_content(routed_response.chosen_extracted_data_json).build()

    async def _route_get_field_chunk_request(
        self,
        request: ParsedRequest,
        edata_source: Optional[ExtractedDataSource],
    ):
        if edata_source == ExtractedDataSource.CORLEONE:
            corleone_task_result = await self._create_corleone_get_field_chunk_task(request)
            extraction_task_result = None

        elif edata_source == ExtractedDataSource.EXTRACTION:
            extraction_task_result = await self._create_extraction_get_field_chunk_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, extraction_task_result = await asyncio.gather(
                self._create_corleone_get_field_chunk_task(request),
                self._create_extraction_get_field_chunk_task(request),
                return_exceptions=True,
            )

        return ExtractedDataRoutedResponse(
            corleone_task_result=corleone_task_result,
            extraction_task_result=extraction_task_result,
        )

    async def _route_get_type_request(
        self,
        request: ParsedRequest,
        type_source: Optional[DocumentTypeSource],
    ) -> TypeRoutedResponse:
        if type_source == DocumentTypeSource.CORLEONE:
            corleone_task_result = await self._create_corleone_get_type_task(request)
            document_type_task_result = None

        elif type_source == DocumentTypeSource.DOCUMENT_TYPE:
            document_type_task_result = await self._create_type_get_type_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, document_type_task_result = await asyncio.gather(
                self._create_corleone_get_type_task(request),
                self._create_type_get_type_task(request),
                return_exceptions=True,
            )
        return TypeRoutedResponse(
            corleone_task_result=corleone_task_result, document_type_task_result=document_type_task_result
        )

    async def _route_get_edata_request(
        self,
        request: ParsedRequest,
        edata_source: Optional[ExtractedDataSource],
    ) -> ExtractedDataRoutedResponse:
        if edata_source == ExtractedDataSource.CORLEONE:
            corleone_task_result = await self._create_corleone_get_edata_task(request)
            extraction_task_result = None

        elif edata_source == ExtractedDataSource.EXTRACTION:
            extraction_task_result = await self._create_extraction_get_edata_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, extraction_task_result = await asyncio.gather(
                self._create_corleone_get_edata_task(request),
                self._create_extraction_get_edata_task(request),
                return_exceptions=True,
            )

        return ExtractedDataRoutedResponse(
            corleone_task_result=corleone_task_result,
            extraction_task_result=extraction_task_result,
        )

    async def _route_delete_edata_fields_request(
        self,
        request: ParsedRequest,
        edata_source: Optional[ExtractedDataSource],
    ) -> ExtractedDataRoutedResponse:
        if edata_source == ExtractedDataSource.CORLEONE:
            corleone_task_result = await self._create_corleone_delete_edata_fields_task(request)
            extraction_task_result = None

        elif edata_source == ExtractedDataSource.EXTRACTION:
            extraction_task_result = await self._create_extraction_delete_edata_fields_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, extraction_task_result = await asyncio.gather(
                self._create_corleone_delete_edata_fields_task(request),
                self._create_extraction_delete_edata_fields_task(request),
                return_exceptions=True,
            )

        return ExtractedDataRoutedResponse(
            corleone_task_result=corleone_task_result,
            extraction_task_result=extraction_task_result,
        )

    async def _route_put_edata_field_request(
        self,
        request: ParsedRequest,
        edata_source: Optional[ExtractedDataSource],
    ) -> ExtractedDataRoutedResponse:
        if edata_source == ExtractedDataSource.CORLEONE:
            corleone_task_result = await self._create_corleone_put_edata_field_task(request)
            extraction_task_result = None

        elif edata_source == ExtractedDataSource.EXTRACTION:
            extraction_task_result = await self._create_extraction_put_edata_field_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, extraction_task_result = await asyncio.gather(
                self._create_corleone_put_edata_field_task(request),
                self._create_extraction_put_edata_field_task(request),
                return_exceptions=True,
            )

        return ExtractedDataRoutedResponse(
            corleone_task_result=corleone_task_result,
            extraction_task_result=extraction_task_result,
        )

    async def _route_update_edata_request(
        self,
        request: ParsedRequest,
        edata_source: Optional[ExtractedDataSource],
    ):
        if edata_source == ExtractedDataSource.CORLEONE:
            corleone_task_result = await self._create_corleone_update_edata_task(request)
            extraction_task_result = None

        elif edata_source == ExtractedDataSource.EXTRACTION:
            extraction_task_result = await self._create_extraction_update_edata_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, extraction_task_result = await asyncio.gather(
                self._create_corleone_update_edata_task(request),
                self._create_extraction_update_edata_task(request),
                return_exceptions=True,
            )

        return ExtractedDataRoutedResponse(
            corleone_task_result=corleone_task_result,
            extraction_task_result=extraction_task_result,
        )

    async def _route_update_edata_cells_request(
        self,
        request: ParsedRequest,
        edata_source: Optional[ExtractedDataSource],
    ):
        if edata_source == ExtractedDataSource.CORLEONE:
            corleone_task_result = await self._create_corleone_update_edata_cells_task(request)
            extraction_task_result = None

        elif edata_source == ExtractedDataSource.EXTRACTION:
            extraction_task_result = await self._create_extraction_update_edata_cells_task(request)
            corleone_task_result = None

        else:
            corleone_task_result, extraction_task_result = await asyncio.gather(
                self._create_corleone_update_edata_cells_task(request),
                self._create_extraction_update_edata_cells_task(request),
                return_exceptions=True,
            )

        return ExtractedDataRoutedResponse(
            corleone_task_result=corleone_task_result,
            extraction_task_result=extraction_task_result,
        )

    async def _create_corleone_get_type_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.get_document_type(**await request.to_dict()))

    async def _create_type_get_type_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._document_type_proxy.get_document_type(
                **await request.change_url(CORLEONE_BASE_API_PREFIX, DOCUMENT_TYPE_BASE_API_PREFIX).to_dict(),
            )
        )

    async def _create_corleone_get_edata_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.get_extracted_data(**await request.to_dict()))

    async def _create_corleone_get_field_chunk_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.get_field_chunk(**await request.to_dict()))

    async def _create_corleone_put_edata_field_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.put_extracted_data_field(**await request.to_dict()))

    async def _create_extraction_get_edata_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._extraction_proxy.get_extracted_data(
                **await request.change_url(CORLEONE_BASE_API_PREFIX, EXTRACTION_BASE_API_PREFIX).to_dict(),
            )
        )

    async def _create_extraction_get_field_chunk_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._extraction_proxy.get_field_chunk(
                **await request.change_url(
                    f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}", f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}"
                ).to_dict(),
            )
        )

    async def _create_corleone_delete_edata_fields_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.delete_extracted_fields(**await request.to_dict()))

    async def _create_extraction_delete_edata_fields_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._extraction_proxy.delete_extracted_fields(
                **await request.change_url(CORLEONE_BASE_API_PREFIX, EXTRACTION_BASE_API_PREFIX).to_dict(),
            )
        )

    async def _create_extraction_put_edata_field_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._extraction_proxy.put_extracted_data_field(
                **await request.change_url(CORLEONE_BASE_API_PREFIX, EXTRACTION_BASE_API_PREFIX).to_dict(),
            )
        )

    async def _create_corleone_update_edata_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.update_extracted_data(**await request.to_dict()))

    async def _create_extraction_update_edata_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._extraction_proxy.update_extracted_data(
                **await request.change_url(CORLEONE_BASE_API_PREFIX, EXTRACTION_BASE_API_PREFIX).to_dict(),
            )
        )

    async def _create_corleone_update_edata_cells_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._corleone_proxy.update_extracted_data_cells(**await request.to_dict()))

    async def _create_extraction_update_edata_cells_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._extraction_proxy.update_extracted_data_cells(
                **await request.change_url(
                    f"{CORLEONE_BASE_API_PREFIX}{V1_PREFIX}", f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}"
                ).to_dict(),
            )
        )

    def _get_type_code_from_type_url(self, url: str) -> str:
        return self._get_last_part_of_url(url)

    async def _register_corleone_plugin(self, request: ParsedRequest):
        request.add_element_in_headers({"content-type": "application/json"})
        response = await self._corleone_proxy.request(**await request.to_dict())
        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .build()
        )

    @staticmethod
    def _get_document_id_from_extracted_data_url(url: str) -> str:
        return re.search(r"/(\d+)(/?)", url)[1]

    @staticmethod
    def _get_last_part_of_url(url: str) -> str:
        return url.split("/")[-1]

    async def _cache_types(self, response: TypesAggregatedResponse) -> None:
        self._update_type_cache(response.corleone, DocumentTypeSource.CORLEONE)
        self._update_type_cache(response.document_type, DocumentTypeSource.DOCUMENT_TYPE)

    def _cache_type(self, response: TypeRoutedResponse) -> None:
        if response.corleone:
            self._update_type_cache([response.corleone], DocumentTypeSource.CORLEONE)

        if response.document_type:
            self._update_type_cache([response.document_type], DocumentTypeSource.DOCUMENT_TYPE)

    def _update_type_cache(self, types: list[TypeContent], source: DocumentTypeSource) -> None:
        for document_type in types:
            self._document_type_source_cache[document_type.code] = source
            self._document_type_extraction_type_cache[document_type.code] = document_type.extraction_type

    def _get_type_source(self, type_code: str) -> Optional[DocumentTypeSource]:
        return self._document_type_source_cache.get(type_code)

    def _get_extracted_data_source(self, document_id: str) -> Optional[ExtractedDataSource]:
        mapping = {
            DocumentTypeSource.CORLEONE: ExtractedDataSource.CORLEONE,
            DocumentTypeSource.DOCUMENT_TYPE: ExtractedDataSource.EXTRACTION,
        }

        document_type_code = self._document_type_code_cache.get(document_id)

        if document_type_code:
            document_type_source = self._get_type_source(document_type_code)

            return mapping.get(document_type_source)

        return None
