from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response
from fastapi import status as http_status

from deps_api_gateway.application import BatchService
from deps_api_gateway.constants import BATCH_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    AddBatchFilesRequest,
    CreateBatchRequest,
    CreateBatchResponse,
    GetBatchesRequest,
    GetBatchesResponse,
    SerializedBatchInfo,
    UpdateBatchRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["batch_router"]

batch_router = APIRouter(prefix=BATCH_ROUTER_PREFIX, tags=["Batches"])


@batch_router.get("", status_code=http_status.HTTP_200_OK, response_model=GetBatchesResponse)
@inject
async def get_batches(
    status: list[str] = Query(default=None),
    get_batches_request: GetBatchesRequest = Depends(),
    batch_service: BatchService = Depends(Provide[Application.batch]),
) -> Response:
    proxy_response = await batch_service.get_batches(
        name=get_batches_request.name,
        status=status,
        group=get_batches_request.group,
        date_start=get_batches_request.date_start,
        date_end=get_batches_request.date_end,
        page=get_batches_request.page,
        per_page=get_batches_request.per_page,
        sort_by=get_batches_request.sort_by,
        sort_order=get_batches_request.sort_order,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.post(
    "",
    status_code=http_status.HTTP_201_CREATED,
    response_model=CreateBatchResponse,
)
@inject
async def create_batch(
    create_batch_request: CreateBatchRequest,
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.create_batch(
        batch_name=create_batch_request.name,
        group_id=create_batch_request.group_id,
        batch_metadata=create_batch_request.metadata,
        file_params=create_batch_request.files,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.get("/{batchId}", response_model=SerializedBatchInfo)
@inject
async def get_batch_info(
    batch_id: str = Path(..., alias="batchId"),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.find_batch(batch_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.patch("/{batchId}")
@inject
async def update_batch(
    data_request: UpdateBatchRequest,
    batch_id: str = Path(..., alias="batchId"),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.update_batch(batch_id=batch_id, name=data_request.name)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.delete("", status_code=http_status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def delete_batches(
    ids: list[str] = Query(...),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.delete_batches(ids=ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.delete("/with-documents", status_code=http_status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def delete_batches_with_documents(
    ids: list[str] = Query(...),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.delete_batches_with_documents(ids=ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.delete(
    "/{batchId}/files",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def delete_files(
    batch_id: str = Path(..., alias="batchId"),
    file_ids: list[str] = Query(..., alias="ids"),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.delete_files(batch_id=batch_id, file_ids=file_ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.delete(
    "/{batchId}/files/with-documents",
    status_code=http_status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def delete_files_with_documents(
    batch_id: str = Path(..., alias="batchId"),
    file_ids: list[str] = Query(..., alias="ids"),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.delete_files_with_documents(batch_id=batch_id, file_ids=file_ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@batch_router.post("/{batchId}/files", status_code=http_status.HTTP_201_CREATED, response_model=None)
@inject
async def add_files(
    add_batch_files_request: AddBatchFilesRequest,
    batch_id: str = Path(..., alias="batchId"),
    batch_service: BatchService = Depends(Provide[Application.batch]),
):
    proxy_response = await batch_service.add_files(batch_id=batch_id, files=add_batch_files_request.files_as_dict)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
