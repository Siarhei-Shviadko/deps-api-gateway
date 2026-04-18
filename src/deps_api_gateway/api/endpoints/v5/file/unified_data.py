from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response

from deps_api_gateway.application import ElementType, FileService
from deps_api_gateway.containers import Application

from ....serializers import SerializedUnifiedData, SerializedUnifiedDataCell
from ....utilities import ResponseBuilder

__all__ = ["unified_data_router"]

unified_data_router = APIRouter()


@unified_data_router.get("/{fileId}/unified-data", response_model=SerializedUnifiedData)
@inject
async def get_unified_data(
    file_id: str = Path(..., alias="fileId"),
    pos_text_blob_name: Optional[str] = Query(None),
    unified_data_types: Optional[set[ElementType]] = Query(None),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.get_unified_data(
        file_id=file_id, pos_text_blob_name=pos_text_blob_name, unified_data_types=unified_data_types
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@unified_data_router.get(
    "/{fileId}/unified-data/tables/{tableId}/cells",
    response_model=list[SerializedUnifiedDataCell],
)
@inject
async def get_unified_cells_data(
    file_id: str = Path(..., alias="fileId"),
    table_id: str = Path(..., alias="tableId"),
    first_column: Optional[int] = Query(default=None, alias="firstColumn"),
    last_column: Optional[int] = Query(default=None, alias="lastColumn"),
    first_row: Optional[int] = Query(default=None, alias="firstRow"),
    last_row: Optional[int] = Query(default=None, alias="lastRow"),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.get_unified_cells_data(
        file_id=file_id,
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
