from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Response, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import SerializedDocument
from ....utilities import ResponseBuilder

__all__ = ["document_type_router"]

document_type_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@document_type_router.post(
    "/{documentId}/assign-type",
    status_code=status.HTTP_200_OK,
    response_model=SerializedDocument,
)
@inject
async def assign_type(
    document_id: str = Path(..., alias="documentId"),
    document_type_id: str = Body(..., alias="documentTypeId", embed=True),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.assign_type(document_id=document_id, document_type_id=document_type_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
