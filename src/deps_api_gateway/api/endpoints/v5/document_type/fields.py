from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application
from deps_api_gateway.domain import ExtractionFieldData

from ....serializers import (
    CreateFieldRequest,
    SerializedField,
    SerializedFields,
    UpdateFieldRequest,
    UpdateFieldsRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["extraction_router"]

extraction_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Extraction Fields"])


@extraction_router.post(
    "/{documentTypeId}/extraction-fields",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedField,
)
@inject
async def create_field(
    create_field_request: CreateFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_field(
        document_type_id=document_type_id,
        name=create_field_request.name,
        field_type=create_field_request.type,
        required=create_field_request.required,
        description=create_field_request.description,
        confidential=create_field_request.confidential,
        read_only=create_field_request.read_only,
        order=create_field_request.order,
        extractor_id=create_field_request.extractor_id,
        field_code=create_field_request.field_code,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extraction_router.patch(
    "/{documentTypeId}/extraction-fields/{fieldCode}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedField,
)
@inject
async def update_field(
    update_field_request: UpdateFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    field_code: str = Path(..., alias="fieldCode"),
    extractor_id: Optional[str] = Query(
        None,
        alias="extractorId",
        description="ID of an extractor containing the field to update. "
        "If not provided every extractor of the document type will be searched.",
    ),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_field(
        document_type_id=document_type_id,
        field_code=field_code,
        name=update_field_request.name,
        required=update_field_request.required,
        description=update_field_request.description,
        confidential=update_field_request.confidential,
        read_only=update_field_request.read_only,
        order=update_field_request.order,
        extractor_id=extractor_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extraction_router.patch(
    "/{documentTypeId}/extraction-fields",
    status_code=status.HTTP_200_OK,
    response_model=SerializedFields,
)
@inject
async def update_fields(
    update_fields_request: UpdateFieldsRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    fields = [ExtractionFieldData(**field.model_dump(by_alias=False)) for field in update_fields_request.fields]
    proxy_response = await application.update_fields(document_type_id=document_type_id, fields=fields)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extraction_router.delete(
    "/{documentTypeId}/extraction-fields",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def delete_field(
    document_type_id: str = Path(..., alias="documentTypeId"),
    field_codes: list[str] = Query(..., alias="fieldCodes"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_fields(
        document_type_id=document_type_id,
        field_codes=field_codes,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
