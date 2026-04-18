from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Request

from deps_api_gateway.application.legacy import WorkflowService
from deps_api_gateway.containers import Application

from ....auth import get_deps_token

__all__ = ["sagas_router"]

sagas_router = APIRouter(prefix="/sagas", tags=["Workflows"])


@sagas_router.get("/{entityId}/state", response_model=str)
@inject
async def get_saga_state(
    request: Request,
    entity_id: str = Path(..., alias="entityId"),
    workflow_service: WorkflowService = Depends(Provide[Application.workflow_old]),
):
    deps_token = get_deps_token(request)
    return await workflow_service.get_saga_state(deps_token, entity_id)
