from fastapi import APIRouter

from deps_api_gateway.constants import BASE_API_V5_PREFIX

from .agentic_ai import agentic_ai_router
from .batch import batch_router
from .csrf import csrf_router
from .document import document_router
from .document_type import document_type_router
from .event_relay import event_relay_router
from .file import file_router
from .groups import groups_router
from .iam import iam_router
from .services import services_router
from .storage import storage_router
from .tools import tools_router
from .workflow_manager import sagas_router, workflow_configuration_router

__all__ = ["v5_router"]

v5_router = APIRouter(prefix=BASE_API_V5_PREFIX)
v5_router.include_router(document_router)
v5_router.include_router(document_type_router)
v5_router.include_router(tools_router)
v5_router.include_router(csrf_router)
v5_router.include_router(iam_router)
v5_router.include_router(groups_router)
v5_router.include_router(storage_router)
v5_router.include_router(batch_router)
v5_router.include_router(event_relay_router)
v5_router.include_router(services_router)
v5_router.include_router(agentic_ai_router)
v5_router.include_router(file_router)
v5_router.include_router(sagas_router)
v5_router.include_router(workflow_configuration_router)
