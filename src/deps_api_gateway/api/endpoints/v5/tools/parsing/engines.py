from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response

from deps_api_gateway.api.serializers.v5.parsing import ParseableEnginesResponse
from deps_api_gateway.api.utilities import ResponseBuilder
from deps_api_gateway.application.parsing import LayoutType
from deps_api_gateway.application.tools import ParsingToolsService
from deps_api_gateway.containers import Application

__all__ = ["engines_router"]

engines_router = APIRouter()


@engines_router.get("/engines", response_model=ParseableEnginesResponse)
@inject
async def get_engines(
    layout_type: LayoutType | None = Query(default=None, alias="layoutType"),
    application: ParsingToolsService = Depends(Provide[Application.tools.parsing]),
) -> Response:
    proxy_response = await application.get_engines(layout_type)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
