from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response

from deps_api_gateway.application import DocumentService, Provider
from deps_api_gateway.containers import Application

from ....serializers.v5 import SerializedAllSemanticLayoutInfo, SerializedSemanticLayout
from ....utilities import ResponseBuilder

__all__ = ["semantic_layout_router"]

semantic_layout_router = APIRouter(prefix="/semantic-layout", tags=["Semantic Layout"])


@semantic_layout_router.get(
    "/{layoutId}",
    status_code=HTTPStatus.OK,
    response_model=SerializedSemanticLayout,
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


@semantic_layout_router.get(
    "/{layoutId}/info",
    status_code=HTTPStatus.OK,
    response_model=SerializedAllSemanticLayoutInfo,
    summary="Retrieve semantic layout metadata for all providers by layout ID.",
)
@inject
async def get_semantic_layout_info(
    layout_id: str = Path(..., alias="layoutId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_semantic_layout_info(layout_id=layout_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
