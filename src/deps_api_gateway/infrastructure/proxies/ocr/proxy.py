import json
from typing import Optional

from aiohttp import FormData
from async_rest_client import Methods
from pydantic import Json
from starlette.datastructures import UploadFile

from deps_api_gateway.application import (
    Bbox,
    IOCRProxy,
    OCREngineEnum,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import OCR_BASE_API_PREFIX, V1_PREFIX, V2_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import OCRError, OCRServiceUnavailableError

__all__ = ["OCRProxy"]


class OCRProxy(GenericRestClient, IOCRProxy):
    v1_prefix = f"{OCR_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{OCR_BASE_API_PREFIX}{V2_PREFIX}"
    exception = OCRError

    async def get_languages(self) -> ProxyResponse:
        url = f"{self.v1_prefix}/languages"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise OCRServiceUnavailableError(error)

    async def get_engines(self) -> ProxyResponse:
        url = f"{self.v2_prefix}/engines"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise OCRServiceUnavailableError(error)

    async def extract_area(
        self,
        engine: OCREngineEnum,
        file_url: str,
        force_ocr: bool = False,
        language: str = "eng",
        area: Optional[Bbox] = None,
        engine_settings: Optional[Json] = None,
    ) -> ProxyResponse:
        if area is None:
            area = {"x": 0, "y": 0, "w": 1, "h": 1}
        if engine_settings is None:
            engine_settings = {}

        url = f"{self.v2_prefix}/extract-area"
        data = {
            "engine": engine.value,
            "blobFile": file_url,
            "forceOCR": force_ocr,
            "language": language,
            "area": area,
            "engineSettings": json.dumps(engine_settings),
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise OCRServiceUnavailableError(error)

    async def extract_text(
        self,
        file: UploadFile,
        engine: OCREngineEnum,
        metadata: Optional[UploadFile] = None,
        language: str = "eng",
        engine_settings: Optional[Json] = None,
    ) -> ProxyResponse:
        if engine_settings is None:
            engine_settings = {}

        url = f"{self.v2_prefix}/extract-text"

        form_data = FormData()
        form_data.add_field(
            "file",
            await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )
        if metadata is not None:
            form_data.add_field(
                "metadata",
                await metadata.read(),
                filename=metadata.filename,
                content_type=metadata.content_type,
            )
        form_data.add_field("engine", engine.value)
        form_data.add_field("language", language)
        form_data.add_field("engineSettings", json.dumps(engine_settings), content_type="application/json")

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data())
            )
        except Exception as error:
            raise OCRServiceUnavailableError(error)

    async def extract_image_page(self, blob_name: str, engine: OCREngineEnum, language: str = "eng") -> ProxyResponse:
        url = f"{self.v2_prefix}/extract-image-page"
        data = {
            "blobName": blob_name,
            "engine": engine,
            "language": language,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise OCRServiceUnavailableError(error)
