from http import HTTPStatus
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, Response

from deps_api_gateway.application import ExtractionService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    SaveExtractedDataRequest,
    SerializedExtractedData,
    TableChunkResponse,
    TableFieldChunk,
)
from ....utilities import ResponseBuilder

__all__ = ["extracted_data_router"]

extracted_data_router = APIRouter(
    prefix=f"{DOCUMENT_ROUTER_PREFIX}/{{documentId}}/extracted-data", tags=["Extracted Data"]
)


@extracted_data_router.patch(
    "/{fieldCode}/aliases",
    status_code=HTTPStatus.OK,
    summary="Update display aliases for List elements. <fieldCode> is the code of the field to update.",
)
@inject
async def update_aliases(
    document_id: str = Path(..., alias="documentId"),
    field_code: str = Path(
        ...,
        alias="fieldCode",
    ),
    aliases: dict[str, str] = Body(
        ...,
        alias="updatedAliases",
        embed=True,
    ),
    application: ExtractionService = Depends(Provide[Application.extraction]),
) -> Response:
    result = await application.update_aliases(document_id=document_id, field_code=field_code, aliases=aliases)

    return (
        ResponseBuilder()
        .with_status(result.status_code)
        .with_headers(dict(result.headers))
        .with_content(result.content)
        .build()
    )


@extracted_data_router.put(
    "",
    status_code=HTTPStatus.OK,
    response_model=SerializedExtractedData,
    description="Save extracted data with extending fields",
)
@inject
async def save_extracted_data(
    extracted_data: SaveExtractedDataRequest,
    document_id: str = Path(..., alias="documentId"),
    application: ExtractionService = Depends(Provide[Application.extraction]),
) -> Response:
    proxy_response = await application.save_extracted_data(
        document_id=document_id, save_extracted_data_dto=extracted_data.to_dto()
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extracted_data_router.put(
    "/override",
    status_code=HTTPStatus.OK,
    response_model=SerializedExtractedData,
    description="Save extracted data with replacing fields values if they are passed. "
    "Not mentioned in request fields will be removed.",
)
@inject
async def save_extracted_data_with_override(
    extracted_data: SaveExtractedDataRequest,
    document_id: str = Path(..., alias="documentId"),
    application: ExtractionService = Depends(Provide[Application.extraction]),
) -> Response:
    proxy_response = await application.save_extracted_data_with_override(
        document_id=document_id, save_extracted_data_dto=extracted_data.to_dto()
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extracted_data_router.patch(
    "/{fieldCode}/table",
    status_code=HTTPStatus.OK,
    response_model=TableFieldChunk,
    summary="Update single table field of extracted data",
)
@inject
async def save_partial_extracted_data(
    field_data: TableFieldChunk,
    document_id: str = Path(..., alias="documentId"),
    field_code: str = Path(..., alias="fieldCode"),
    application: ExtractionService = Depends(Provide[Application.extraction]),
) -> Response:
    """
    Must contain exactly 1 source coordinates
    """
    proxy_response = await application.save_partial_extracted_data_field(
        document_id=document_id, field_code=field_code, field_data=field_data.to_dto()
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extracted_data_router.get(
    "/{fieldCode}/table/chunk",
    status_code=HTTPStatus.OK,
    response_model=TableChunkResponse,
    summary="Get paginated extracted data of a table field",
)
@inject
async def get_table_field_chunk(
    document_id: str = Path(..., alias="documentId"),
    field_code: str = Path(..., alias="fieldCode"),
    rows_per_chunk: int = Query(..., alias="rowsPerChunk", ge=1),
    rows_chunk: int = Query(..., alias="rowsChunk", ge=1),
    list_index: Optional[int] = Query(None, alias="listIndex", ge=0),
    application: ExtractionService = Depends(Provide[Application.extraction]),
) -> Response:
    proxy_response = await application.get_table_field_chunk(
        document_id=document_id,
        field_code=field_code,
        rows_per_chunk=rows_per_chunk,
        rows_chunk=rows_chunk,
        list_index=list_index,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
