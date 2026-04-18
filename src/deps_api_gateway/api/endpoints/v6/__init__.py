from fastapi import APIRouter

from deps_api_gateway.constants import BASE_API_V6_PREFIX

from .document import document_router

__all__ = ["v6_router"]

v6_router = APIRouter(prefix=BASE_API_V6_PREFIX)
v6_router.include_router(document_router)
