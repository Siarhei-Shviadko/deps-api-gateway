from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, status

from deps_api_gateway.application.legacy import EnrichmentService
from deps_api_gateway.containers import Application

from ....serializers.v1 import SaveSupplementRequest
from ....utilities import ResponseBuilder

__all__ = ["supplement_router"]

supplement_router = APIRouter(tags=["Documents"])


@supplement_router.put(
    "/documents/{documentId}/supplements",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
@inject
async def create_or_modify_supplement(
    supplement: SaveSupplementRequest,
    document_id: str = Path(..., alias="documentId"),
    enrichment_service: EnrichmentService = Depends(Provide[Application.enrichment]),
):
    response = await enrichment_service.create_or_modify_supplement(
        document_id=document_id,
        document_type_id=supplement.document_type_id,
        extra_data=supplement.get_raw_data(),
    )
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )


@supplement_router.get(
    "/documents/{documentId}/supplements",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
@inject
async def find_supplement(
    document_id: str = Path(..., alias="documentId"),
    enrichment_service: EnrichmentService = Depends(Provide[Application.enrichment]),
):
    response = await enrichment_service.find_supplement(document_id)
    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )
