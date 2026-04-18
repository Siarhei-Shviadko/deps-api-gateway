from http import HTTPStatus
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import NonNegativeInt

from deps_api_gateway.application import FileService, ParsingFeature, ParsingType
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    SerializedDocumentLayout,
    SerializedParsingInfo,
    SerializedTabularLayout,
    UpdateImageRequest,
    UpdateKeyValuePairRequest,
    UpdateParagraphRequest,
    UpdateTableRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["parsing_router"]

parsing_router = APIRouter(prefix="/{fileId}")


@parsing_router.get(
    "/parsing-info",
    status_code=HTTPStatus.OK,
    response_model=SerializedParsingInfo,
    summary="Retrieve layout information for a specific file by ID.",
)
@inject
async def get_file_info(
    file_id: str = Path(..., alias="fileId"),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    result = await application.get_parsing_info(file_id)

    return (
        ResponseBuilder()
        .with_status(result.status_code)
        .with_headers(dict(result.headers))
        .with_content(result.content)
        .build()
    )


@parsing_router.get(
    "/document-layout",
    status_code=HTTPStatus.OK,
    response_model=SerializedDocumentLayout,
    summary="Retrieve detailed document layout information for a file.",
)
@inject
async def get_file_layout(
    file_id: str = Path(..., alias="fileId"),
    parsing_type: ParsingType = Query(..., alias="parsingType"),
    features: Optional[set[ParsingFeature]] = Query(default=None),
    batch_index: Optional[int] = Query(None, ge=0, alias="batchIndex"),
    batch_size: Optional[int] = Query(None, ge=1, alias="batchSize"),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.get_file_layout(
        file_id=file_id,
        parsing_type=parsing_type,
        features=features,
        batch_index=batch_index,
        batch_size=batch_size,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@parsing_router.get(
    "/tabular-layout",
    status_code=HTTPStatus.OK,
    response_model=SerializedTabularLayout,
    summary="Retrieve detailed tabular layout information for a file.",
)
@inject
async def get_tabular_layout(
    file_id: str = Path(..., alias="fileId"),
    tables: Optional[list[str]] = Query(
        None, description="List of table IDs to filter the cells by. If omitted, cells from all tables are returned."
    ),
    row_span: Optional[tuple[NonNegativeInt, NonNegativeInt]] = Query(
        None,
        description="A tuple that represents the range of rows to be used for filtering cells. "
        + "The rows are indexed starting from 0, and both the start and end indices are inclusive.",
        alias="rowSpan",
    ),
    col_span: Optional[tuple[NonNegativeInt, NonNegativeInt]] = Query(
        None,
        description="A tuple that represents the range of columns to be used for filtering cells. "
        + "The columns are indexed starting from 0, and both the start and end indices are inclusive.",
        alias="colSpan",
    ),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.get_tabular_layout(
        file_id=file_id,
        tables=tables,
        row_span=row_span,
        col_span=col_span,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@parsing_router.put(
    "/document-layout/user-parsing-type",
    status_code=HTTPStatus.OK,
    response_model=SerializedParsingInfo,
    summary="Create copy of document layout with USER_DEFINED parsing type.",
)
@inject
async def clone_document_layout(
    file_id: str = Path(..., alias="fileId"),
    parsing_type: str = Body(..., validation_alias="parsingType", alias="parsingType", embed=True),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    result = await application.clone_document_layout(file_id=file_id, parsing_type=parsing_type)

    return (
        ResponseBuilder()
        .with_status(result.status_code)
        .with_headers(dict(result.headers))
        .with_content(result.content)
        .build()
    )


@parsing_router.patch(
    "/document-layout/pages/{pageId}/paragraphs/{paragraphId}",
    status_code=HTTPStatus.OK,
    response_class=Response,
)
@inject
async def update_paragraph(
    update_paragraph_request: UpdateParagraphRequest,
    file_id: str = Path(..., alias="fileId"),
    page_id: str = Path(..., alias="pageId"),
    paragraph_id: str = Path(..., alias="paragraphId"),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.update_paragraph(
        file_id=file_id,
        page_id=page_id,
        paragraph_id=paragraph_id,
        update_paragraph_request=update_paragraph_request.model_dump(by_alias=True),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@parsing_router.patch(
    "/document-layout/pages/{pageId}/images/{imageId}",
    status_code=HTTPStatus.OK,
)
@inject
async def update_image(
    data: UpdateImageRequest,
    file_id: str = Path(..., alias="fileId"),
    page_id: str = Path(..., alias="pageId"),
    image_id: str = Path(..., alias="imageId"),
    application: FileService = Depends(Provide[Application.file]),
) -> None:
    proxy_response = await application.update_document_layout_image(
        file_id=file_id,
        page_id=page_id,
        image_id=image_id,
        title=data.title,
        description=data.description,
        polygon=data.polygon,
        filepath=data.filepath,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@parsing_router.patch(
    "/document-layout/pages/{pageId}/tables/{tableId}",
    status_code=HTTPStatus.OK,
    response_class=Response,
)
@inject
async def update_table(
    update_table_request: UpdateTableRequest,
    file_id: str = Path(..., alias="fileId"),
    page_id: str = Path(..., alias="pageId"),
    table_id: str = Path(..., alias="tableId"),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.update_table(
        file_id=file_id,
        page_id=page_id,
        table_id=table_id,
        update_table_request=update_table_request.model_dump(by_alias=True),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@parsing_router.patch(
    "/document-layout/pages/{pageId}/key-value-pairs/{keyValuePairId}",
    status_code=HTTPStatus.OK,
    response_class=Response,
)
@inject
async def update_key_value_pair(
    update_key_value_pair_request: UpdateKeyValuePairRequest,
    file_id: str = Path(..., alias="fileId"),
    page_id: str = Path(..., alias="pageId"),
    key_value_pair_id: str = Path(..., alias="keyValuePairId"),
    application: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await application.update_key_value_pair(
        file_id=file_id,
        page_id=page_id,
        key_value_pair_id=key_value_pair_id,
        update_key_value_pair_request=update_key_value_pair_request.model_dump(exclude_unset=True, by_alias=True),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
