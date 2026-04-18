from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_api_gateway.api.serializers import EnginesResponse
from deps_api_gateway.api.utilities import ResponseBuilder
from deps_api_gateway.application.tools import OCRService
from deps_api_gateway.containers import Application

__all__ = ["engines_router"]

engines_router = APIRouter()


@engines_router.get("/engines", response_model=EnginesResponse)
@inject
async def get_engines(
    application: OCRService = Depends(Provide[Application.tools.ocr]),
) -> Response:
    proxy_response = await application.get_engines()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
