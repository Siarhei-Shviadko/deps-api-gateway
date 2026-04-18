from fastapi import APIRouter

from .engines import engines_router
from .extract_text import extract_text_router
from .languages import languages_router

__all__ = ["ocr_router"]

ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])
ocr_router.include_router(languages_router)
ocr_router.include_router(engines_router)
ocr_router.include_router(extract_text_router)
