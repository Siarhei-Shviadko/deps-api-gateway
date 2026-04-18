from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application
from deps_api_gateway.domain import ExtraFieldData

from ....serializers.v5.enrichment import (
    SaveExtraFieldResponse,
    UpdateExtraFieldsRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["enrichment_router"]


enrichment_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Enrichment Data"])


@enrichment_router.post(
    "/{documentTypeId}/extra-fields",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    response_model=SaveExtraFieldResponse,
)
@inject
async def save_extra_fields(
    document_type_id: str = Path(..., alias="documentTypeId"),
    name: str = Body(...),
    display_order: int = Body(default=0, validation_alias="order", alias="order"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.save_extra_fields(
        document_type_id=document_type_id,
        name=name,
        order=display_order,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@enrichment_router.put(
    "/{documentTypeId}/extra-fields",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=SaveExtraFieldResponse,
)
@inject
async def update_extra_fields(
    request: UpdateExtraFieldsRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    fields = [ExtraFieldData(**model.model_dump()) for model in request.extra_fields]
    proxy_response = await application.update_extra_fields(
        document_type_id=document_type_id,
        fields=fields,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@enrichment_router.delete(
    "/{documentTypeId}/extra-fields",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
@inject
async def delete_extra_fields(
    document_type_id: str = Path(..., alias="documentTypeId"),
    extra_field_codes: list[str] = Query(..., alias="extraFieldCodes"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_extra_fields(
        document_type_id=document_type_id,
        extra_field_codes=extra_field_codes,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
