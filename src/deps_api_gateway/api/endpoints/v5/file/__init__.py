from .file import file_router
from .parsing import parsing_router
from .unified_data import unified_data_router

__all__ = ["file_router"]

file_router.include_router(unified_data_router)
file_router.include_router(parsing_router)
