from fastapi import APIRouter

from deps_api_gateway.constants import API_PREFIX, BASE_API_V1_PREFIX

from .document import document_router
from .document_types import document_types_router, old_document_types_router
from .enrichment import extra_field_router, supplement_router
from .parsing import parsing_router
from .prompter import prompter_router
from .prototype import prototype_router
from .workflow import sagas_router

__all__ = ["v1_router"]

v1_router = APIRouter()

v1_router.include_router(document_router, prefix=API_PREFIX)
v1_router.include_router(document_types_router, prefix=BASE_API_V1_PREFIX)
v1_router.include_router(parsing_router, prefix=API_PREFIX)
v1_router.include_router(prototype_router, prefix=API_PREFIX)
v1_router.include_router(sagas_router, prefix=API_PREFIX)
v1_router.include_router(supplement_router, prefix=BASE_API_V1_PREFIX)
v1_router.include_router(extra_field_router, prefix=BASE_API_V1_PREFIX)
v1_router.include_router(prompter_router, prefix=BASE_API_V1_PREFIX)
v1_router.include_router(old_document_types_router, prefix=API_PREFIX)
