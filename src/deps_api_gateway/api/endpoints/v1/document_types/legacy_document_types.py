from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Request

from deps_api_gateway.application.legacy import DocumentTypeOldService
from deps_api_gateway.constants import ExtractionType
from deps_api_gateway.containers import Application

from ....auth import get_deps_token

__all__ = ["old_document_types_router"]

old_document_types_router = APIRouter(prefix="/document-types", tags=["Legacy Document Types API"])


@old_document_types_router.get("", response_model=list[dict[str, Any]], deprecated=True)
@inject
async def get_document_types(
    request: Request,
    extraction_type: Optional[ExtractionType] = Query(None, alias="extractionType"),
    document_type_service: DocumentTypeOldService = Depends(Provide[Application.document_type_oldest]),
):
    deps_token = get_deps_token(request)
    return await document_type_service.get_document_types(deps_token, extraction_type)


@old_document_types_router.get("/{typeId}", response_model=dict[str, Any], deprecated=True)
@inject
async def get_document_type(
    request: Request,
    type_id: str = Path(..., alias="typeId"),
    document_type_service: DocumentTypeOldService = Depends(Provide[Application.document_type_oldest]),
):
    deps_token = get_deps_token(request)
    return await document_type_service.get_document_type(type_id, deps_token)
