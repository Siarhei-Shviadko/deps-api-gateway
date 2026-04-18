from urllib.parse import urlparse

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from deps_api_gateway.application.legacy import DocumentService, WorkflowService
from deps_api_gateway.containers import Application

from ....auth import get_deps_token
from ....serializers import (
    AggregatedDocumentList,
    DocumentListFilterRequest,
    ImportDocumentsRequest,
)

__all__ = ["document_router"]

document_router = APIRouter(prefix="/documents", tags=["Documents"])


@document_router.get("", response_model=AggregatedDocumentList)
@inject
async def get_document_list(
    request: Request,
    filter_: DocumentListFilterRequest = Depends(),
    document_service: DocumentService = Depends(Provide[Application.document_old]),
):
    deps_token = get_deps_token(request)
    query_string = urlparse(str(request.url)).query
    filter_ = filter_.to_model(raw_query=query_string)  # type: ignore
    return await document_service.get_documents(filter_, deps_token)


@document_router.post("/import")
@inject
async def import_documents(
    request: Request,
    import_documents_request: ImportDocumentsRequest,
    workflow_service: WorkflowService = Depends(Provide[Application.workflow_old]),
):
    deps_token = get_deps_token(request)
    await workflow_service.import_documents(
        data=import_documents_request.to_dto(),
        deps_token=deps_token,
    )
