from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import GetStatesResponse
from ....utilities import ResponseBuilder

states_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@states_router.get("/states", response_model=GetStatesResponse, status_code=status.HTTP_200_OK)
@inject
async def get_document_states(
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_document_states()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
