from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentService, SaveExtraDataElement
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    SaveSupplementRequest,
    SaveSupplementResponse,
    SerializedSupplement,
)
from ....utilities import ResponseBuilder

__all__ = ["supplement_router"]

supplement_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Enrichment Data"])


@supplement_router.get("/{documentId}/supplement", status_code=status.HTTP_200_OK, response_model=SerializedSupplement)
@inject
async def get_document_supplement(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_document_supplement(document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@supplement_router.put(
    "/{documentId}/supplement",
    status_code=status.HTTP_200_OK,
    response_model=SaveSupplementResponse,
)
@inject
async def save_document_supplement(
    supplement_data: SaveSupplementRequest,
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.save_document_supplement(
        document_id=document_id,
        document_type_id=supplement_data.document_type_id,
        extra_data_list=[SaveExtraDataElement(**element) for element in supplement_data.model_dump()["data"]],
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
