from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response

from deps_api_gateway.application import DocumentService, ElementType
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import SerializedUnifiedData, SerializedUnifiedDataCell
from ....utilities import ResponseBuilder

__all__ = ["unified_data_router"]

unified_data_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Unified Data"])


@unified_data_router.get("/{documentId}/unified-data", response_model=SerializedUnifiedData)
@inject
async def get_unified_data(
    document_id: str = Path(..., alias="documentId"),
    pos_text_blob_name: Optional[str] = Query(None),
    unified_data_types: Optional[set[ElementType]] = Query(None),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_unified_data(
        document_id=document_id, pos_text_blob_name=pos_text_blob_name, unified_data_types=unified_data_types
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@unified_data_router.get(
    "/{document_id}/unified-data/tables/{table_id}/cells",
    response_model=list[SerializedUnifiedDataCell],
)
@inject
async def get_unified_cells_data(
    document_id: str,
    table_id: str,
    first_column: Optional[int] = Query(default=None, alias="firstColumn"),
    last_column: Optional[int] = Query(default=None, alias="lastColumn"),
    first_row: Optional[int] = Query(default=None, alias="firstRow"),
    last_row: Optional[int] = Query(default=None, alias="lastRow"),
    application: DocumentService = Depends(Provide[Application.document]),
):
    proxy_response = await application.get_unified_cells_data(
        document_id=document_id,
        table_id=table_id,
        cells_reference={
            "firstColumn": first_column,
            "lastColumn": last_column,
            "firstRow": first_row,
            "lastRow": last_row,
        },
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
