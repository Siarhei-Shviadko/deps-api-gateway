from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    AssignLLMToLLMExtractorRequest,
    AssignLLMToLLMExtractorResponse,
    AttachLLMExtractorRequest,
    AttachLLMExtractorResponse,
    MoveQueriesRequest,
    SerializedExtractionQuery,
    SerializedLLMWorkflow,
    UpdateLLMExtractorRequest,
    UpdateLLMExtractorResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["llm_extractor_router"]

llm_extractor_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["LLM Extractors"])


@llm_extractor_router.post(
    "/{documentTypeId}/llm-extractors/{extractorId}/extraction-query",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedExtractionQuery,
)
@inject
async def add_extraction_query(
    extraction_query_data: SerializedExtractionQuery,
    document_type_id: str = Path(..., alias="documentTypeId"),
    extractor_id: str = Path(..., alias="extractorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.add_extraction_query(
        document_type_id=document_type_id,
        extractor_id=extractor_id,
        code=extraction_query_data.code,
        shape=extraction_query_data.shape.to_dict(),
        workflow=extraction_query_data.workflow.to_dict(),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@llm_extractor_router.patch(
    "/{documentTypeId}/llm-extractors/{extractorId}/extraction-query/{code}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedExtractionQuery,
)
@inject
async def update_extraction_query(
    code: str,
    workflow: SerializedLLMWorkflow = Body(..., embed=True),
    document_type_id: str = Path(..., alias="documentTypeId"),
    extractor_id: str = Path(..., alias="extractorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_extraction_query(
        document_type_id=document_type_id,
        extractor_id=extractor_id,
        code=code,
        workflow=workflow.to_dict(),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@llm_extractor_router.post(
    "/llm-extractor",
    status_code=status.HTTP_201_CREATED,
    response_model=AttachLLMExtractorResponse,
    description="Find or create a document type by name and attach an llm extractor to it.\n"
    "Can only attach LLM type extractors.",
)
@inject
async def create_llm_extractor(
    extractor_request: AttachLLMExtractorRequest,
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_llm_extractor(
        extractor_name=extractor_request.extractor_name,
        document_type_name=extractor_request.document_type_name,
        provider=extractor_request.provider,
        model=extractor_request.model,
        extractor_id=extractor_request.extractor_id,
        extraction_params=extractor_request.extraction_params.to_dict(),
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@llm_extractor_router.put(
    "/{documentTypeId}/llm-extractors/{extractorId}",
    status_code=status.HTTP_200_OK,
    response_model=UpdateLLMExtractorResponse,
    description="Update LLM extractor parameters.",
)
@inject
async def update_llm_extractor(
    request: UpdateLLMExtractorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    extractor_id: str = Path(..., alias="extractorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_llm_extractor(
        extractor_id=extractor_id,
        document_type_id=document_type_id,
        name=request.name,
        extraction_params=request.extraction_params.to_dict(),
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@llm_extractor_router.put(
    "/{documentTypeId}/llm-extractors/{extractorId}/llm",
    status_code=status.HTTP_200_OK,
    response_model=AssignLLMToLLMExtractorResponse,
    description="Update LLM of an extractor.",
)
@inject
async def assign_llm_to_llm_extractor(
    request: AssignLLMToLLMExtractorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    extractor_id: str = Path(..., alias="extractorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.assign_llm_to_llm_extractor(
        extractor_id=extractor_id,
        document_type_id=document_type_id,
        provider=request.provider,
        model=request.model,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@llm_extractor_router.post(
    "/{documentTypeId}/llm-extractors/move-queries",
    status_code=status.HTTP_200_OK,
)
@inject
async def move_queries_between_extractors(
    request: MoveQueriesRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> None:
    proxy_response = await application.move_queries_between_extractors(
        source_extractor_id=request.source_extractor_id,
        target_extractor_id=request.target_extractor_id,
        document_type_id=document_type_id,
        fields_codes=request.fields_codes,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
