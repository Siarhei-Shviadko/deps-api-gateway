from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Request, Response, status

from deps_api_gateway.application.legacy import PrototypeService
from deps_api_gateway.containers import Application

from ....auth import get_deps_token

__all__ = ["prototype_router"]

prototype_router = APIRouter(prefix="/prototypes", tags=["Prototype"])


@prototype_router.get("/{prototypeId}/layouts", response_model=dict[str, Any])
@inject
async def find_layouts(
    prototype_id: str = Path(..., alias="prototypeId"),
    prototype_service: PrototypeService = Depends(Provide[Application.prototype]),
) -> dict[str, Any]:
    return await prototype_service.find_layouts(prototype_id)


@prototype_router.get("/{prototypeId}/layouts/{layoutId}", response_model=dict[str, Any])
@inject
async def find_layout(
    request: Request,
    prototype_id: str = Path(..., alias="prototypeId"),
    layout_id: str = Path(..., alias="layoutId"),
    prototype_service: PrototypeService = Depends(Provide[Application.prototype]),
) -> dict[str, Any]:
    deps_token = get_deps_token(request)
    return await prototype_service.find_layout(prototype_id, layout_id, deps_token)


@prototype_router.delete(
    "/{prototypeId}/layouts/{layoutId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_reference_layout(
    prototype_id: str = Path(..., alias="prototypeId"),
    layout_id: str = Path(..., alias="layoutId"),
    prototype_service: PrototypeService = Depends(Provide[Application.prototype]),
) -> None:
    await prototype_service.delete_layout(prototype_id=prototype_id, layout_id=layout_id)


@prototype_router.delete(
    "/{prototypeId}/layouts",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_reference_layouts(
    layout_ids: list[str] = Query(..., alias="layoutIds"),
    prototype_id: str = Path(..., alias="prototypeId"),
    prototype_service: PrototypeService = Depends(Provide[Application.prototype]),
) -> None:
    await prototype_service.delete_layouts(prototype_id=prototype_id, layout_ids=layout_ids)
