from fastapi import APIRouter

from deps_api_gateway.constants import BASE_API_PREFIX

from .debug import debug_router
from .v1 import v1_router
from .v5 import v5_router
from .v6 import v6_router

__all__ = ["router"]

router = APIRouter()
router.include_router(debug_router, prefix=BASE_API_PREFIX)
router.include_router(v5_router)
router.include_router(v6_router)
router.include_router(v1_router)
