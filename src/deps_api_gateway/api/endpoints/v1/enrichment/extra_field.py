from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application.legacy import EnrichmentService
from deps_api_gateway.containers import Application

from ....serializers import SaveExtraFieldRequest, UpdateExtraFieldsRequest
from ....utilities import ResponseBuilder

__all__ = ["extra_field_router"]

extra_field_router = APIRouter(tags=["Document Types"])


@extra_field_router.post(
    "/document-types/{documentTypeId}/extra-fields", status_code=status.HTTP_201_CREATED, response_model=dict[str, str]
)
@inject
async def create_extra_field(
    extra_field: SaveExtraFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    enrichment_service: EnrichmentService = Depends(Provide[Application.enrichment]),
):
    response = await enrichment_service.create_extra_field(
        document_type_id=document_type_id,
        name=extra_field.name,
        display_order=extra_field.display_order,
    )
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )


@extra_field_router.delete(
    "/document-types/{documentTypeId}/extra-fields",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_extra_fields(
    document_type_id: str = Path(..., alias="documentTypeId"),
    extra_field_codes: list[str] = Query(..., alias="extraFieldCodes"),
    enrichment_service: EnrichmentService = Depends(Provide[Application.enrichment]),
):
    response = await enrichment_service.delete_extra_fields(document_type_id, extra_field_codes)
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )


@extra_field_router.get("/document-types/{documentTypeId}/extra-fields", response_model=dict[str, Any])
@inject
async def get_extra_fields(
    document_type_id: str = Path(..., alias="documentTypeId"),
    enrichment_service: EnrichmentService = Depends(Provide[Application.enrichment]),
):
    response = await enrichment_service.get_extra_fields(document_type_id)
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )


@extra_field_router.put(
    "/document-types/{documentTypeId}/extra-fields",
    status_code=status.HTTP_200_OK,
)
@inject
async def update_extra_fields(
    extra_fields: UpdateExtraFieldsRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    enrichment_service: EnrichmentService = Depends(Provide[Application.enrichment]),
):
    response = await enrichment_service.update_extra_fields(
        document_type_id=document_type_id, extra_fields=extra_fields.model_dump(by_alias=True)
    )
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )
