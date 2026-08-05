from fastapi import APIRouter

from .engines import engines_router

__all__ = ["parsing_router"]

parsing_router = APIRouter(prefix="/parsing", tags=["Parsing"])
parsing_router.include_router(engines_router)
