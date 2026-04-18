import asyncio
import re
from enum import Enum
from functools import partial
from typing import Awaitable, Callable, Optional, Union

from async_rest_client import Methods
from cachetools import TTLCache
from fastapi.responses import Response

from deps_api_gateway.api.utilities import (
    ParsedRequest,
    ResponseBuilder,
    UnifiedDataRoutedResponse,
)
from deps_api_gateway.application.legacy import IPreprocess, IUnifier
from deps_api_gateway.constants import (
    PREPROCESS_BASE_API_PREFIX,
    UNIFIER_BASE_API_PREFIX,
    V1_PREFIX,
    DocumentTypeSource,
    UnifiedDataSource,
)
from deps_api_gateway.infrastructure import OldGenericRestClient

from .abstract_router import AbstractRouter, RequestMapper

TaskResult = Union[dict, BaseException]

__all__ = ["PreprocessRouter"]


class _UdataType(Enum):
    UNIFIED_DATA = "unified_data"
    TABLE_CELLS = "table_cells"


class PreprocessRouter(AbstractRouter):
    def __init__(
        self,
        client: OldGenericRestClient,
        preprocess_proxy: IPreprocess,
        unifier_proxy: IUnifier,
        document_type_source_cache: TTLCache,
        document_type_code_cache: TTLCache,
    ) -> None:
        super().__init__(client)
        self._preprocess_proxy = preprocess_proxy
        self._unifier_proxy = unifier_proxy
        self._document_type_source_cache = document_type_source_cache
        self._document_type_code_cache = document_type_code_cache

        self._unifier_task_mapping: dict[_UdataType, Callable[[ParsedRequest], Awaitable[TaskResult]]] = {
            _UdataType.UNIFIED_DATA: self._create_unifier_get_udata_task,
            _UdataType.TABLE_CELLS: self._create_unifier_get_table_cells_task,
        }

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (
                Methods.GET,
                rf"^{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}/unified_data/deprecated/\d+$",
            ): partial(self._get_unified_data, udata_type=_UdataType.UNIFIED_DATA),
            (
                Methods.GET,
                rf"^{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}/unified_data/\d+$",
            ): partial(self._get_unified_data, udata_type=_UdataType.UNIFIED_DATA),
            (
                Methods.GET,
                rf"^{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}/preprocessed-table-data/\d+/\w+$",
            ): partial(self._get_unified_data, udata_type=_UdataType.TABLE_CELLS),
        }

    async def _get_unified_data(self, request: ParsedRequest, *, udata_type: _UdataType) -> Response:
        document_id, _ = self._get_ids_from_unified_data_url(request.url)
        unified_data_source = self._get_unified_data_source(document_id)

        routed_response = await self._route_get_udata_request(request, unified_data_source, udata_type)
        return (
            ResponseBuilder()
            .with_content(routed_response.chosen_unified_data_json)
            .with_status(routed_response.status_code)
            .build()
        )

    async def _route_get_udata_request(
        self,
        request: ParsedRequest,
        udata_source: Optional[UnifiedDataSource],
        udata_type: _UdataType,
    ) -> UnifiedDataRoutedResponse:
        unifier_task_maker = self._unifier_task_mapping[udata_type]

        if udata_source == UnifiedDataSource.PREPROCESS:
            preprocess_task_result = await self._create_preprocess_get_task(request)
            unifier_task_result = None

        elif udata_source == UnifiedDataSource.UNIFIER:
            unifier_task_result = await unifier_task_maker(request)
            preprocess_task_result = None

        else:
            preprocess_task_result, unifier_task_result = await asyncio.gather(
                self._create_preprocess_get_task(request),
                unifier_task_maker(request),
                return_exceptions=True,
            )

        return UnifiedDataRoutedResponse(
            preprocess_task_result=preprocess_task_result,
            unifier_task_result=unifier_task_result,
        )

    async def _create_preprocess_get_task(self, request: ParsedRequest):
        return await asyncio.create_task(self._preprocess_proxy.get_unified_data(**await request.to_dict()))

    async def _create_unifier_get_udata_task(self, request: ParsedRequest):
        return await asyncio.create_task(
            self._unifier_proxy.get_unified_data(
                **await request.change_url(
                    f"{PREPROCESS_BASE_API_PREFIX}{V1_PREFIX}", f"{UNIFIER_BASE_API_PREFIX}{V1_PREFIX}"
                ).to_dict(),
            )
        )

    async def _create_unifier_get_table_cells_task(self, request: ParsedRequest):
        document_id, table_id = self._get_ids_from_unified_data_url(request.url)

        return await asyncio.create_task(
            self._unifier_proxy.get_unified_data(
                **{  # type: ignore
                    **await request.to_dict(),
                    "url": f"{UNIFIER_BASE_API_PREFIX}{V1_PREFIX}/unified_data/{document_id}/tables/{table_id}/cells",
                },
            )
        )

    @staticmethod
    def _get_ids_from_unified_data_url(url: str) -> tuple[str, Union[str, None]]:
        match = re.match(r"^.*\/(?P<document_id>\d+)(\/(?P<table_id>\w+)$|$)", url)
        if not match:
            raise ValueError("Not valid url")

        return match.group("document_id"), match.group("table_id")

    def _get_unified_data_source(self, document_id: str) -> Optional[UnifiedDataSource]:
        mapping = {
            DocumentTypeSource.CORLEONE: UnifiedDataSource.PREPROCESS,
            DocumentTypeSource.DOCUMENT_TYPE: UnifiedDataSource.UNIFIER,
        }

        document_type_code = self._document_type_code_cache.get(document_id)

        if document_type_code:
            document_type_source = self._document_type_source_cache.get(document_type_code)

            return mapping.get(document_type_source)

        return None
