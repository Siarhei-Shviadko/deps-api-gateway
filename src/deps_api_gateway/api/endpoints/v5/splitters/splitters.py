from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response
from fastapi import status as http_status

from deps_api_gateway.application import SplittingService
from deps_api_gateway.constants import SPLITTER_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    CreateSplitterRequest,
    CreateSplitterResponse,
    FindSplitterForRequest,
    FindSplitterForResponse,
    FindSplitterResponse,
    FindSplittersRequest,
    FindSplittersResponse,
    UpdateSplitterRequest,
    UpdateSplitterResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["splitting_router"]

splitting_router = APIRouter(prefix=SPLITTER_ROUTER_PREFIX, tags=["Splitting"])


@splitting_router.get("", status_code=http_status.HTTP_200_OK, response_model=FindSplittersResponse)
@inject
async def find_splitters(
    request: FindSplittersRequest = Depends(),
    splitter_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitter_service.find_splitters(group_id=request.group_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_router.get("/resolve", status_code=http_status.HTTP_200_OK, response_model=FindSplitterForResponse)
@inject
async def find_splitter_for(
    request: FindSplitterForRequest = Depends(),
    splitter_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitter_service.find_splitter_for(
        group_id=request.group_id,
        document_type_id=request.document_type_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_router.get("/{splitterId}", status_code=http_status.HTTP_200_OK, response_model=FindSplitterResponse)
@inject
async def find_splitter(
    splitter_id: str = Path(..., alias="splitterId"),
    splitter_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitter_service.find_splitter(splitter_id=splitter_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_router.post("", status_code=http_status.HTTP_201_CREATED, response_model=CreateSplitterResponse)
@inject
async def create_splitter(
    request: CreateSplitterRequest,
    splitter_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitter_service.create_splitter(
        data=request.model_dump(by_alias=True, exclude_none=True),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_router.patch("/{splitterId}", status_code=http_status.HTTP_200_OK, response_model=UpdateSplitterResponse)
@inject
async def update_splitter(
    request: UpdateSplitterRequest,
    splitter_id: str = Path(..., alias="splitterId"),
    splitter_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitter_service.update_splitter(
        splitter_id=splitter_id,
        data=request.model_dump(by_alias=True, exclude_none=True),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@splitting_router.delete("/{splitterId}", status_code=http_status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def remove_splitter(
    splitter_id: str = Path(..., alias="splitterId"),
    splitter_service: SplittingService = Depends(Provide[Application.splitter]),
) -> Response:
    proxy_response = await splitter_service.remove_splitter(splitter_id=splitter_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
