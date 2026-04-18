from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response

from deps_api_gateway.application import DocumentService, Provider
from deps_api_gateway.containers import Application

from ....utilities import ResponseBuilder

__all__ = ["semantic_layout_router"]

semantic_layout_router = APIRouter(prefix="/semantic-layout", tags=["Semantic Layout Parsing"])


@semantic_layout_router.get(
    "/{layoutId}",
    status_code=HTTPStatus.OK,
    summary="Retrieve semantic layout information by layout ID.",
)
@inject
async def get_semantic_layout(
    layout_id: str = Path(..., alias="layoutId"),
    provider: Provider = Query(default=Provider.LLAMAINDEX),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_semantic_layout(layout_id=layout_id, provider=provider)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
