from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from .....serializers.v5 import (
    CreateMappingRequest,
    CreateTabularMappingRequest,
    ModifyMappingRequest,
    SerializedMapping,
    SerializedTabularMapping,
    UpdateTabularMappingRequest,
)
from .....utilities import ResponseBuilder

__all__ = ["mapping_router"]

mapping_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Prototype Extractors"])


@mapping_router.post(
    "/{documentTypeId}/prototype/mappings",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedMapping,
)
@inject
async def create_mapping(
    data: CreateMappingRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_mapping(
        document_type_id=document_type_id,
        code=data.code,
        keys=data.keys,
        data_type=data.data_type,
        mapping_type=data.mapping_type,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@mapping_router.put(
    "/{documentTypeId}/prototype/mappings/{fieldCode}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedMapping,
)
@inject
async def update_mapping(
    data: ModifyMappingRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    field_code: str = Path(..., alias="fieldCode"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_mapping(
        document_type_id=document_type_id,
        code=field_code,
        keys=data.keys,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@mapping_router.post(
    "/{documentTypeId}/prototype/tabular-mappings",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedTabularMapping,
)
@inject
async def create_tabular_mapping(
    data: CreateTabularMappingRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_tabular_mapping(
        code=data.code,
        document_type_id=document_type_id,
        header_type=data.header_type,
        headers=[header.to_dict() for header in data.headers],
        occurrence_index=data.occurrence_index,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@mapping_router.patch(
    "/{documentTypeId}/prototype/tabular-mappings/{code}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedTabularMapping,
)
@inject
async def update_tabular_mapping(
    data: UpdateTabularMappingRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    code: str = Path(...),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_tabular_mapping(
        document_type_id=document_type_id,
        code=code,
        header_type=data.header_type,
        headers=[header.to_dict() for header in data.headers] if data.headers is not None else None,
        occurrence_index=data.occurrence_index,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
