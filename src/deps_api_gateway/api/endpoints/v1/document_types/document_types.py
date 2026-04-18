from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path

from deps_api_gateway.application.legacy import DocumentTypeService, ExtractionService
from deps_api_gateway.containers import Application

from ....serializers import (
    CreateDocumentTypeRequest,
    CreateExtractionFieldRequest,
    DocumentTypeResponseData,
    DocumentTypesResponseData,
    UpdateDocumentTypeLLMRequest,
    UpdateExtractionFieldRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["document_types_router"]

document_types_router = APIRouter(prefix="/document-types", tags=["Document Types"])


@document_types_router.put("/{documentTypeId}/llm", response_model=dict[str, Any])
@inject
async def update_document_type_llm(
    update_document_type_llm_request: UpdateDocumentTypeLLMRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    document_type_service: DocumentTypeService = Depends(Provide[Application.document_type_old]),
):
    response = await document_type_service.update_document_type_llm(
        type_id=document_type_id,
        llm_data=update_document_type_llm_request.model_dump(by_alias=False),
    )

    return (
        ResponseBuilder()
        .with_content(response["content"])
        .with_status(response["status_code"])
        .with_headers(response["headers"])
        .build()
    )


@document_types_router.post("", response_model=dict[str, Any])
@inject
async def create_document_type(
    document_type_data: CreateDocumentTypeRequest,
    document_type_service: DocumentTypeService = Depends(Provide[Application.document_type_old]),
):
    response = await document_type_service.create_document_type(
        name=document_type_data.name,
        description=document_type_data.description,
    )

    return (
        ResponseBuilder()
        .with_status(response.status_code)
        .with_headers(response.headers)
        .with_content(response.content)
        .build()
    )


@document_types_router.post("/{documentTypeId}/extraction-fields", response_model=dict[str, Any])
@inject
async def create_extraction_field(
    create_extraction_field_request: CreateExtractionFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: ExtractionService = Depends(Provide[Application.extraction_old]),
):
    response = await application.create_extraction_field(
        document_type_id=document_type_id,
        name=create_extraction_field_request.name,
        field_type=create_extraction_field_request.type,
        required=create_extraction_field_request.required,
        confidential=create_extraction_field_request.confidential,
        read_only=create_extraction_field_request.read_only,
        description=create_extraction_field_request.description,
        order=create_extraction_field_request.order,
        extractor_id=create_extraction_field_request.extractor_id,
        field_code=create_extraction_field_request.field_code,
    )

    return (
        ResponseBuilder()
        .with_status(response.status_code)
        .with_headers(response.headers)
        .with_content(response.content)
        .build()
    )


@document_types_router.get("", response_model=DocumentTypesResponseData)
@inject
async def get_document_types(
    document_type_service: DocumentTypeService = Depends(Provide[Application.document_type_old]),
):
    response = await document_type_service.get_document_types()
    return DocumentTypesResponseData.from_response(response)


@document_types_router.get("/{documentTypeId}", response_model=dict[str, Any])
@inject
async def get_document_type(
    document_type_id: str = Path(..., alias="documentTypeId"),
    document_type_service: DocumentTypeService = Depends(Provide[Application.document_type_old]),
):
    response = await document_type_service.get_document_type(document_type_id=document_type_id)
    return DocumentTypeResponseData.from_response(response).model_dump(by_alias=True)


@document_types_router.patch("/{documentTypeId}/extraction-fields/{fieldCode}", response_model=dict[str, Any])
@inject
async def update_extraction_field(
    update_extraction_field_request: UpdateExtractionFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    field_code: str = Path(..., alias="fieldCode"),
    application: ExtractionService = Depends(Provide[Application.extraction_old]),
):
    response = await application.update_extraction_field(
        document_type_id=document_type_id,
        code=field_code,
        name=update_extraction_field_request.name,
        required=update_extraction_field_request.required,
        confidential=update_extraction_field_request.confidential,
        read_only=update_extraction_field_request.read_only,
        description=update_extraction_field_request.description,
        order=update_extraction_field_request.order,
    )

    return (
        ResponseBuilder()
        .with_status(response.status_code)
        .with_headers(response.headers)
        .with_content(response.content)
        .build()
    )
