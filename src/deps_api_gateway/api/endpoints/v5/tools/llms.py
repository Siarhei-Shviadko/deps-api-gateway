from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_api_gateway.application.tools import AIFusionService
from deps_api_gateway.containers import Application

from ....serializers import LLMSResponse
from ....utilities import ResponseBuilder

__all__ = ["llms_router"]

llms_router = APIRouter(tags=["LLM Analysis"])


@llms_router.get("/llms", response_model=LLMSResponse)
@inject
async def get_engines(
    application: AIFusionService = Depends(Provide[Application.tools.ai_fusion]),
) -> Response:
    proxy_response = await application.get_llms()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
