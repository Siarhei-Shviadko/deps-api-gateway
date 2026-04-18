from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from deps_api_gateway.application import WorkflowService
from deps_api_gateway.containers import Application

from ....utilities import ResponseBuilder

__all__ = ["sagas_router"]

sagas_router = APIRouter(prefix="/sagas", tags=["Workflow Manager"])


@sagas_router.get("/{entityId}/state", response_model=str)
@inject
async def get_saga_state(
    entity_id: str = Path(..., alias="entityId"),
    workflow_service: WorkflowService = Depends(Provide[Application.workflow]),
):
    proxy_response = await workflow_service.get_saga_state(entity_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
