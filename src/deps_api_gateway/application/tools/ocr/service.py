from typing import Optional

from pydantic import Json
from starlette.datastructures import UploadFile

from ...proxy_response import ProxyResponse
from ...types import Bbox
from .consolidator import OCRConsolidator
from .engine import OCREngineEnum
from .proxy import IOCRProxy

__all__ = ["OCRService"]


class OCRService:
    def __init__(
        self,
        ocr_proxy: IOCRProxy,
    ) -> None:
        self._ocr_proxy = ocr_proxy

    async def get_languages(self) -> ProxyResponse:
        return OCRConsolidator.get_languages_from(await self._ocr_proxy.get_languages())

    async def get_engines(self) -> ProxyResponse:
        return OCRConsolidator.get_engines_from(await self._ocr_proxy.get_engines())

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
        return await self._ocr_proxy.extract_area(
            engine=engine,
            file_url=file_url,
            force_ocr=force_ocr,
            language=language,
            area=area,
            engine_settings=engine_settings,
        )

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
        return OCRConsolidator.extract_text_from(
            await self._ocr_proxy.extract_text(
                file=file, metadata=metadata, engine=engine, language=language, engine_settings=engine_settings
            )
        )

    async def extract_image_page(self, blob_name: str, engine: OCREngineEnum, language: str = "eng") -> ProxyResponse:
        return await self._ocr_proxy.extract_image_page(
            blob_name=blob_name,
            engine=engine,
            language=language,
        )
