from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application import DocumentTypeExtras, DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX, ExtractionType
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    DocumentTypesResponse,
    GetDocumentTypeResponse,
    UpdateDocumentTypeLLMRequest,
    UpdateDocumentTypeLLMResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["document_types_router"]


document_types_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Document Types"])


@document_types_router.get("", status_code=status.HTTP_200_OK, response_model=DocumentTypesResponse)
@inject
async def get_document_types(
    extraction_type: Optional[ExtractionType] = Query(default=None, alias="extractionType"),
    workflow_configurations: Optional[bool] = Query(default=False, alias="workflowConfigurations"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_document_types(
        extraction_type=extraction_type, workflow_configurations=workflow_configurations
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_types_router.get("/{documentTypeId}", status_code=status.HTTP_200_OK, response_model=GetDocumentTypeResponse)
@inject
async def get_document_type(
    document_type_id: str = Path(..., alias="documentTypeId"),
    extras: Optional[list[DocumentTypeExtras]] = Query(default=None),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_document_type(document_type_id=document_type_id, extras=extras)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_types_router.delete("/{documentTypeId}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def delete_document_type(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
):
    proxy_response = await application.delete_document_type(document_type_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@document_types_router.put(
    "/{documentTypeId}/llm",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=UpdateDocumentTypeLLMResponse,
    description="[Deprecated] Associate the default LLM Extraction with a Document Type. Have to use LLM Extractors API instead.",
    deprecated=True,
)
@inject
async def update_document_type_llm(
    request: UpdateDocumentTypeLLMRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_document_type_llm(
        document_type_id=document_type_id,
        llm_type=request.llm_type,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
