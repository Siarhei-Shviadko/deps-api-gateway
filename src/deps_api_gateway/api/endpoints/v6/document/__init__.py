from fastapi import APIRouter

from .document import documents_router

__all__ = ["document_router"]

document_router = APIRouter()
document_router.include_router(documents_router)
