from fastapi import APIRouter

from deps_api_gateway.constants import AGENTIC_AI_ROUTER_PREFIX

from .agent_vendor import agent_vendors_router
from .agentic_manifest import manifests_router
from .conversation import conversations_router
from .mode import modes_router
from .sse import sse_conversations_router

__all__ = ["agentic_ai_router"]


agentic_ai_router = APIRouter(prefix=AGENTIC_AI_ROUTER_PREFIX, tags=["Agentic AI"])
agentic_ai_router.include_router(agent_vendors_router)
agentic_ai_router.include_router(conversations_router)
agentic_ai_router.include_router(manifests_router)
agentic_ai_router.include_router(sse_conversations_router)
agentic_ai_router.include_router(modes_router)
