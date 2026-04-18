from fastapi import APIRouter

from deps_api_gateway.constants import IAM_ROUTER_PREFIX

from .organisations import organisation_router
from .users import users_router

__all__ = ["iam_router"]

iam_router = APIRouter(prefix=IAM_ROUTER_PREFIX)
iam_router.include_router(users_router)
iam_router.include_router(organisation_router)
