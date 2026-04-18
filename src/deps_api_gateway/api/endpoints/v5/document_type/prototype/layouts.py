from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Path, Query, Response, UploadFile, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from .....serializers.v5 import (
    CreateReferenceLayoutResponse,
    GetReferenceLayoutsResponse,
)
from .....utilities import ResponseBuilder

__all__ = ["layout_router"]

layout_router = APIRouter(
    prefix=f"{DOCUMENT_TYPE_ROUTER_PREFIX}/{{documentTypeId}}/prototype/layouts", tags=["Prototype Extractors"]
)


@layout_router.get("", status_code=status.HTTP_200_OK, response_model=GetReferenceLayoutsResponse)
@inject
async def get_reference_layouts(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_reference_layouts(document_type_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@layout_router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateReferenceLayoutResponse)
@inject
async def create_reference_layout(
    document_type_id: str = Path(..., alias="documentTypeId"),
    file: UploadFile = File(...),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_reference_layout(document_type_id=document_type_id, file=file)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@layout_router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
@inject
async def delete_reference_layouts(
    document_type_id: str = Path(..., alias="documentTypeId"),
    layout_ids: list[str] = Query(..., alias="layoutIds"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_reference_layouts(
        document_type_id=document_type_id, layout_ids=layout_ids
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@layout_router.post(
    "/{layoutId}/pipelines/restart",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
@inject
async def restart_reference_layout(
    document_type_id: str = Path(..., alias="documentTypeId"),
    layout_id: str = Path(..., alias="layoutId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.restart_reference_layout(document_type_id=document_type_id, layout_id=layout_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@layout_router.get(
    "/{layoutId}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
@inject
async def get_reference_layout(
    document_type_id: str = Path(..., alias="documentTypeId"),
    layout_id: str = Path(..., alias="layoutId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_reference_layout(document_type_id=document_type_id, layout_id=layout_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
