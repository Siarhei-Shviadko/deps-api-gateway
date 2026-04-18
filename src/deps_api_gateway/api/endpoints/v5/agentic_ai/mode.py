from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from deps_api_gateway.application import AgenticAIService
from deps_api_gateway.containers import Application

from ....serializers.v5 import GetModesResponse
from ....utilities import ResponseBuilder

__all__ = ["modes_router"]

modes_router = APIRouter(prefix="/modes", tags=["Modes"])


@modes_router.get("", status_code=status.HTTP_200_OK, response_model=GetModesResponse)
@inject
async def get_modes(
    application: AgenticAIService = Depends(Provide[Application.agentic_ai]),
) -> Response:
    proxy_response = await application.get_modes()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
