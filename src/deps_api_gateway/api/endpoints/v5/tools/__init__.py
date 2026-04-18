from fastapi import APIRouter

from .llms import llms_router
from .ocr import ocr_router

__all__ = ["tools_router"]

tools_router = APIRouter(prefix="/tools")
tools_router.include_router(ocr_router)
tools_router.include_router(llms_router)
