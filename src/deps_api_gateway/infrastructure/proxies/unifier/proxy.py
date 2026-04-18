from typing import Optional, Union

from async_rest_client import Methods

from deps_api_gateway.application import (
    CellsReference,
    ElementType,
    IUnifierProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import UNIFIER_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import UnifierError, UnifierServiceUnavailableError

__all__ = ["UnifierProxy"]


class UnifierProxy(GenericRestClient, IUnifierProxy):
    v1_prefix = f"{UNIFIER_BASE_API_PREFIX}{V1_PREFIX}"
    exception = UnifierError

    async def get_unified_data(
        self,
        document_id: str,
        pos_text_blob_name: Optional[str] = None,
        unified_data_types: Optional[set[ElementType]] = None,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/unified_data/{document_id}"

        params: dict[str, Union[str, list[str]]] = {}
        if pos_text_blob_name is not None:
            params["pos_text_blob_name"] = pos_text_blob_name
        if unified_data_types is not None:
            params["unified_data_types"] = [unified_data_type.value for unified_data_type in unified_data_types]

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=url, params=params)
            )
        except Exception as error:
            raise UnifierServiceUnavailableError(error)

    async def get_unified_cells_data(
        self,
        document_id: str,
        table_id: str,
        reference: CellsReference,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/unified_data/{document_id}/tables/{table_id}/cells"
        params = {key: value for key, value in reference.items() if value is not None}

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=url, params=params)
            )
        except Exception as error:
            raise UnifierServiceUnavailableError(error)
