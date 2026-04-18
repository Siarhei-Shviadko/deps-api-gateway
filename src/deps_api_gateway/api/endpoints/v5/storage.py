from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, Form, Query, Response, UploadFile, status

from deps_api_gateway.application import StorageService
from deps_api_gateway.containers import Application
from deps_api_gateway.settings import get_storage_settings

from ...serializers import DownloadFileResponse, UploadFileResponse
from ...utilities import ResponseBuilder

__all__ = ["storage_router"]

storage_router = APIRouter(prefix="/file", tags=["Storage"])


@storage_router.get("/{path:path}", status_code=status.HTTP_200_OK, response_model=DownloadFileResponse)
@inject
async def download_file(
    path: str,
    storage: str = Query(default=get_storage_settings().default_storage),
    application: StorageService = Depends(Provide[Application.storage]),
) -> Response:
    proxy_response = await application.download_file(
        path=path,
        storage=storage,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@storage_router.post("", status_code=status.HTTP_201_CREATED, response_model=UploadFileResponse)
@inject
async def upload_file_with_unique_path(
    file: UploadFile = File(...),
    storage: str = Form(default=get_storage_settings().default_storage),
    application: StorageService = Depends(Provide[Application.storage]),
) -> Response:
    proxy_response = await application.upload_file_with_unique_path(
        file_name=file.filename,
        content=file.file.read(),
        storage_name=storage,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@storage_router.delete("/{path:path}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def delete_file(
    path: str,
    storage: str = Form(default=get_storage_settings().default_storage),
    application: StorageService = Depends(Provide[Application.storage]),
) -> Response:
    proxy_response = await application.delete_file(
        path=path,
        storage=storage,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
