from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query

from deps_api_gateway.application import PageBatch, ParsingFeature, ParsingType
from deps_api_gateway.application.legacy import ParsingService
from deps_api_gateway.containers import Application

__all__ = ["parsing_router"]

parsing_router = APIRouter(prefix="/document-layout", tags=["Documents"])


@parsing_router.get("/{documentLayoutId}/pages", response_model=dict[str, Any])
@inject
async def get_pages(
    document_layout_id: str = Path(..., alias="documentLayoutId"),
    parsing_type: ParsingType = Query(..., alias="parsingType"),
    features: Optional[set[ParsingFeature]] = Query(default=None),
    batch_index: int = Query(PageBatch.index, ge=PageBatch.index, alias="batchIndex"),
    batch_size: int = Query(PageBatch.size, ge=PageBatch.size, alias="batchSize"),
    application: ParsingService = Depends(Provide[Application.parsing_old]),
) -> dict[str, Any]:
    return await application.get_pages(
        document_layout_id=document_layout_id,
        parsing_type=parsing_type,
        features=set() if features is None else features,
        batch_index=batch_index,
        batch_size=batch_size,
    )
