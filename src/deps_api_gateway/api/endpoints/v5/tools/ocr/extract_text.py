from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Response, UploadFile
from pydantic import Json

from deps_api_gateway.application.tools import OCREngineEnum, OCRService
from deps_api_gateway.containers import Application

from .....serializers.v5.ocr import (
    ExtractImagePageResponse,
    ExtractTextResponse,
    SerializedBbox,
    SerializedWordBox,
)
from .....utilities import ResponseBuilder

__all__ = ["extract_text_router"]

extract_text_router = APIRouter()


@extract_text_router.post("/extract-area", response_model=SerializedWordBox)
@inject
async def extract_area(
    engine: OCREngineEnum = Body(...),
    file_url: str = Body(..., validation_alias="blobFile", alias="blobFile"),
    force_ocr: bool = Body(default=False, validation_alias="forceOCR", alias="forceOCR"),
    language: str = Body("eng"),
    area: SerializedBbox = Body(
        default=SerializedBbox(x=0, y=0, w=1, h=1),
        description="Area of image that should be extracted if you need to crop image. Relative coordinates",
    ),
    engine_settings: Json = Body({}, embed=True, validation_alias="engineSettings", alias="engineSettings"),
    application: OCRService = Depends(Provide[Application.tools.ocr]),
) -> Response:
    proxy_response = await application.extract_area(
        engine=engine,
        file_url=file_url,
        force_ocr=force_ocr,
        language=language,
        area=area.model_dump(),
        engine_settings=engine_settings,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extract_text_router.post("/extract-text", response_model=ExtractTextResponse)
@inject
async def extract_text(
    file: UploadFile = File(...),
    metadata: Optional[UploadFile] = File(None),
    engine: OCREngineEnum = Body(...),
    language: str = Body("eng"),
    engine_settings: Json = Body({}, embed=True, validation_alias="engineSettings", alias="engineSettings"),
    application: OCRService = Depends(Provide[Application.tools.ocr]),
) -> Response:
    proxy_response = await application.extract_text(
        file=file, metadata=metadata, engine=engine, language=language, engine_settings=engine_settings
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@extract_text_router.post("/extract-image-page", response_model=ExtractImagePageResponse)
@inject
async def extract_image_page(
    blob_name: str = Body(..., alias="blobName"),
    engine: OCREngineEnum = Body(...),
    language: str = Body("eng"),
    application: OCRService = Depends(Provide[Application.tools.ocr]),
) -> Response:
    proxy_response = await application.extract_image_page(blob_name=blob_name, engine=engine, language=language)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
