from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application import DocumentService
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    AddLabelOnDocumentRequest,
    CreateLabelRequest,
    DocumentListNoMetaResponse,
    GetLabelsResponse,
    SerializedDocument,
    SerializedLabel,
)
from ....utilities import ResponseBuilder

__all__ = ["labels_router"]

labels_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@labels_router.get("/labels", response_model=GetLabelsResponse, status_code=status.HTTP_200_OK)
@inject
async def get_labels(
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_labels()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@labels_router.delete("/{documentId}/labels/{labelId}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_label_from_document(
    document_id: str = Path(..., alias="documentId"),
    label_id: str = Path(..., alias="labelId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.remove_label_from_document(document_id=document_id, label_id=label_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@labels_router.post("/labels", response_model=SerializedLabel, status_code=status.HTTP_200_OK)
@inject
async def create_label(
    label_data: CreateLabelRequest,
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.create_label(label_name=label_data.label_name)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@labels_router.post("/{documentId}/labels", response_model=SerializedDocument, status_code=status.HTTP_200_OK)
@inject
async def add_label_on_document(
    label_data: AddLabelOnDocumentRequest,
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.add_label_on_document(document_id=document_id, label_id=label_data.label_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@labels_router.post("/attach-labels", response_model=DocumentListNoMetaResponse, status_code=status.HTTP_200_OK)
@inject
async def add_label_on_documents_batch(
    label_data: AddLabelOnDocumentRequest,
    document_ids: list[str] = Query(..., alias="documentIds"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.add_label_on_documents_batch(
        document_ids=document_ids,
        label_id=label_data.label_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
