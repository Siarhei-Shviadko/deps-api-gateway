from typing import Optional, Protocol

from pydantic import Json
from starlette.datastructures import UploadFile

from ...proxy_response import ProxyResponse
from ...types import Bbox
from .engine import OCREngineEnum

__all__ = ["IOCRProxy"]


class IOCRProxy(Protocol):
    async def get_languages(self) -> ProxyResponse:
        ...

    async def get_engines(self) -> ProxyResponse:
        ...

    async def extract_area(
        self,
        engine: OCREngineEnum,
        file_url: str,
        force_ocr: bool = False,
        language: str = "eng",
        area: Optional[Bbox] = None,
        engine_settings: Optional[Json] = None,
    ) -> ProxyResponse:
        ...

    async def extract_text(
        self,
        file: UploadFile,
        engine: OCREngineEnum,
        metadata: Optional[UploadFile] = None,
        language: str = "eng",
        engine_settings: Optional[Json] = None,
    ) -> ProxyResponse:
        ...

    async def extract_image_page(self, blob_name: str, engine: OCREngineEnum, language: str = "eng") -> ProxyResponse:
        ...
