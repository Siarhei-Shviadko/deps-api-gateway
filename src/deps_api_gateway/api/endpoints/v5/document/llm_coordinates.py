from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.containers import Application

from ....serializers import FieldCodes
from ....utilities import ResponseBuilder

llm_coordinates_router = APIRouter(prefix="/llm-coordinates", tags=["LLM Coordinates"])


@llm_coordinates_router.post(
    "/{entityId}",
    status_code=status.HTTP_200_OK,
)
@inject
async def add_llm_coordinates(
    entity_id: str = Path(..., alias="entityId"),
    field_codes: FieldCodes = Body(...),
    application: DocumentService = Depends(Provide[Application.document]),
) -> None:
    proxy_response = await application.add_llm_coordinates(entity_id, field_codes.codes)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
