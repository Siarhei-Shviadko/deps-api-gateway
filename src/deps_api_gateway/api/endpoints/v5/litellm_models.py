from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_api_gateway.application.tools import LiteLLMService
from deps_api_gateway.containers import Application

from ...utilities import ResponseBuilder

__all__ = ["litellm_models_router"]

litellm_models_router = APIRouter(tags=["LLM Analysis"])


@litellm_models_router.get("/litellm/models")
@inject
async def get_litellm_models(
    application: LiteLLMService = Depends(Provide[Application.tools.litellm]),
) -> Response:
    proxy_response = await application.get_models()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
