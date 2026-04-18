from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status
from fastapi.responses import FileResponse

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....utilities import ResponseBuilder

__all__ = ["files_router"]

files_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@files_router.get("/{documentId}/files", status_code=status.HTTP_200_OK, response_class=FileResponse)
@inject
async def download_original_files(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.download_original_files(document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@files_router.get(
    "/{documentId}/preprocessed-files",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    deprecated=True,
    description="[Deprecated] Preprocessed files endpoint is "
    "working on previous DEPS backend 'corleone', not working on a new backend.",
)
@inject
async def download_preprocessed_files(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.download_preprocessed_files(document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
