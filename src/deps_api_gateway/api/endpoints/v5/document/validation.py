from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import SerializedValidationResult
from ....utilities import ResponseBuilder

__all__ = ["validation_router"]

validation_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Data Validation"])


@validation_router.get("/{documentId}/validation-result", response_model=SerializedValidationResult)
@inject
async def get_validation_result(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_validation_result(document_id=document_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
