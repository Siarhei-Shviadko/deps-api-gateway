from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Response, UploadFile, status
from pydantic import Json

from deps_api_gateway.application import DocumentService, NeedsReviewOption
from deps_api_gateway.constants import DOCUMENT_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import CreateDocumentResponse
from ....utilities import ResponseBuilder

__all__ = ["documents_router"]

documents_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@documents_router.post(
    "/import",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=None,
    summary="Import documents",
    description="Import documents from an external source. documentType is required.",
)
@inject
async def import_documents(
    paths: list[str],
    source: str = Body(...),
    document_type_id: str = Body(..., validation_alias="documentType", alias="documentType"),
    engine: Optional[str] = Body(default=None),
    language: Optional[str] = Body(default=None),
    llm_type: Optional[str] = Body(default=None, validation_alias="llmType", alias="llmType"),
    invoke_unifier: bool = Body(default=True, validation_alias="invokeUnifier", alias="invokeUnifier"),
    invoke_extraction: bool = Body(default=True, validation_alias="invokeExtraction", alias="invokeExtraction"),
    invoke_parsing: Optional[bool] = Body(default=None, validation_alias="invokeParsing", alias="invokeParsing"),
    parsing_features: Optional[list[str]] = Body(
        default=[], validation_alias="parsingFeatures", alias="parsingFeatures"
    ),
    invoke_validation: Optional[bool] = Body(
        default=None, validation_alias="invokeValidation", alias="invokeValidation"
    ),
    invoke_review: Optional[NeedsReviewOption] = Body(
        default=None, validation_alias="invokeReview", alias="invokeReview"
    ),
    invoke_output_exporting: Optional[bool] = Body(
        default=None, validation_alias="invokeOutputExporting", alias="invokeOutputExporting"
    ),
    assign_to_me: bool = Body(default=False, validation_alias="assignedToMe", alias="assignedToMe"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.import_documents(
        paths=paths,
        source=source,
        document_type_id=document_type_id,
        engine=engine,
        language=language,
        llm_type=llm_type,
        needs_parsing=invoke_parsing,
        parsing_features=parsing_features,
        needs_validation=invoke_validation,
        needs_review=invoke_review,
        needs_output_exporting=invoke_output_exporting,
        needs_unifier=invoke_unifier,
        needs_extraction=invoke_extraction,
        assign_to_me=assign_to_me,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    response_model=CreateDocumentResponse,
    summary="Create document",
    description="Create a new document. documentType is required.",
)
@inject
async def create_document(
    document_name: str = Body(..., validation_alias="documentName", alias="documentName"),
    document_type_id: str = Body(..., validation_alias="documentType", alias="documentType"),
    group_id: Optional[str] = Body(default=None, validation_alias="groupId", alias="groupId"),
    file: UploadFile = File(...),
    engine: Optional[str] = Body(default=None),
    language: Optional[str] = Body(default=None),
    llm_type: Optional[str] = Body(default=None, validation_alias="llmType", alias="llmType"),
    parsing_features: Optional[Json] = Body(default=None, validation_alias="parsingFeatures", alias="parsingFeatures"),
    needs_unification: bool = Body(default=True, validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(default=True, validation_alias="needsExtraction", alias="needsExtraction"),
    needs_parsing: Optional[bool] = Body(default=None, validation_alias="needsParsing", alias="needsParsing"),
    needs_validation: Optional[bool] = Body(default=None, validation_alias="needsValidation", alias="needsValidation"),
    needs_review: Optional[NeedsReviewOption] = Body(default=None, validation_alias="needsReview", alias="needsReview"),
    needs_output_exporting: Optional[bool] = Body(
        default=None, validation_alias="needsOutputExporting", alias="needsOutputExporting"
    ),
    assign_to_me: bool = Body(default=False, validation_alias="assignedToMe", alias="assignedToMe"),
    label_ids: Optional[Json] = Body(default=None, validation_alias="labelIds", alias="labelIds"),
    metadata: Optional[Json] = Body(default=None),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.create_document(
        document_name=document_name,
        document_type_id=document_type_id,
        group_id=group_id,
        file=file,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsing_features,
        needs_unification=needs_unification,
        needs_extraction=needs_extraction,
        needs_parsing=needs_parsing,
        needs_validation=needs_validation,
        needs_review=needs_review,
        needs_output_exporting=needs_output_exporting,
        assign_to_me=assign_to_me,
        metadata=metadata,
        label_ids=label_ids,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
