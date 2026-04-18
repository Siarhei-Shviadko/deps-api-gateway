from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import ExtractDataRequest, SerializedDocument
from ....utilities import ResponseBuilder

__all__ = ["extract_data_router"]

extract_data_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@extract_data_router.post(
    "/extract-data",
    response_model=SerializedDocument,
)
@inject
async def extract_data(
    extract_data_request: ExtractDataRequest,
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.extract_data(
        document_ids=extract_data_request.document_ids,
        engine=extract_data_request.engine,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
