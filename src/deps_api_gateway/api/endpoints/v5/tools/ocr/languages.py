from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from deps_api_gateway.api.serializers import LanguagesResponse
from deps_api_gateway.api.utilities import ResponseBuilder
from deps_api_gateway.application.tools import OCRService
from deps_api_gateway.containers import Application

__all__ = ["languages_router"]

languages_router = APIRouter()


@languages_router.get("/languages", response_model=LanguagesResponse)
@inject
async def get_languages(
    application: OCRService = Depends(Provide[Application.tools.ocr]),
) -> Response:
    proxy_response = await application.get_languages()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
