from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application import DocumentTypeService, GetPrototypeExtras
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from .....serializers.v5 import (
    CreatePrototypeRequest,
    CreatePrototypeResponse,
    SerializedPrototype,
    UpdatePrototypeRequest,
    UpdatePrototypeResponse,
)
from .....utilities import ResponseBuilder

__all__ = ["prototype_router"]

prototype_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Prototype Extractors"])


@prototype_router.get(
    "/{documentTypeId}/prototype",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedPrototype,
)
@inject
async def get_prototype(
    document_type_id: str = Path(..., alias="documentTypeId"),
    extras: Optional[list[GetPrototypeExtras]] = Query(default=None),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_prototype(document_type_id=document_type_id, extras=extras)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@prototype_router.post(
    "/prototype",
    status_code=status.HTTP_201_CREATED,
    response_model=CreatePrototypeResponse,
    description="Create a document type with the Prototype Extractor",
)
@inject
async def create_prototype(
    prototype_data: CreatePrototypeRequest,
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_prototype(
        name=prototype_data.name,
        engine=prototype_data.engine,
        language=prototype_data.language,
        description=prototype_data.description,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@prototype_router.patch(
    "/{documentTypeId}/prototype",
    status_code=status.HTTP_200_OK,
    response_model=UpdatePrototypeResponse,
    description="Update a document type with the Prototype Extractor",
)
@inject
async def update_prototype(
    prototype_data: UpdatePrototypeRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_prototype(
        document_type_id=document_type_id,
        engine=prototype_data.engine,
        language=prototype_data.language,
        description=prototype_data.description,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
