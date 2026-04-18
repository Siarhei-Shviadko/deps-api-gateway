import logging
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)
from pydantic import Json

from deps_api_gateway.application import (
    DocumentDetailExtras,
    DocumentService,
    NeedsReviewOption,
    ParsingFeature,
    Status,
)
from deps_api_gateway.constants import (
    DOCUMENT_ROUTER_PREFIX,
    V5_DOCUMENT_CREATE_IMPORT_DEPRECATION_WARNING,
)
from deps_api_gateway.containers import Application

from ....serializers import (
    CreateDocumentResponse,
    DocumentDetailResponse,
    DocumentListFilter,
    DocumentListResponse,
    PartialUpdateDocumentRequest,
    PositiveInt32,
    SerializedDocument,
    SerializedDocumentMetadata,
    SerializedExtractedData,
    ShortDocumentResponse,
)
from ....utilities import ResponseBuilder

__all__ = ["documents_router"]

logger = logging.getLogger(__name__)
documents_router = APIRouter(prefix=DOCUMENT_ROUTER_PREFIX, tags=["Documents"])


@documents_router.get(
    "",
    response_model=DocumentListResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_document_list(
    filter_data: DocumentListFilter = Depends(),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_document_list(filter_data.to_dto())

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.get(
    "/{documentId}",
    response_model=DocumentDetailResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_document_detail(
    document_id: str = Path(..., alias="documentId"),
    extras: Optional[list[DocumentDetailExtras]] = Query(None),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_document_detail(document_id=document_id, extras=extras)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.patch(
    "/{documentId}",
    response_model=ShortDocumentResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def partial_update_document(
    document_data: PartialUpdateDocumentRequest,
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.partial_update_document(
        document_id=document_id, document_data=document_data.to_dto()
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.delete("", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def delete_document_list(
    document_ids: list[PositiveInt32] = Query(alias="documentIds", min_length=1),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.delete_document_list(list(map(str, document_ids)))

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.get(
    "/{documentId}/metadata", status_code=status.HTTP_200_OK, response_model=SerializedDocumentMetadata
)
@inject
async def get_document_metadata(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_document_metadata(document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.get(
    "/{documentId}/extracted-data",
    status_code=status.HTTP_200_OK,
    response_model=SerializedExtractedData,
)
@inject
async def get_extracted_data(
    document_id: str = Path(..., alias="documentId"),
    rows_per_chunk: Optional[int] = Query(None, alias="rowsPerChunk"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.get_extracted_data(document_id=document_id, rows_per_chunk=rows_per_chunk)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


def _get_parsing_features(
    parsing_features: Json = Body([], alias="parsingFeatures"),
) -> list[str]:
    return list({feature for feature in parsing_features}) if parsing_features else []


@documents_router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    response_model=None,
    deprecated=True,
)
@inject
async def upload_document(
    document_name: str = Body(..., validation_alias="documentName", alias="documentName"),
    file: UploadFile = File(...),
    document_type_id: Optional[str] = Body(default=None, validation_alias="documentType", alias="documentType"),
    engine: Optional[str] = Body(default=None),
    language: Optional[str] = Body(default=None),
    llm_type: Optional[str] = Body(default=None, validation_alias="llmType", alias="llmType"),
    parsing_features: list[str] = Depends(_get_parsing_features),
    needs_unifier: bool = Body(default=True, validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(default=True, validation_alias="needsExtraction", alias="needsExtraction"),
    assign_to_me: bool = Body(default=False, validation_alias="assignedToMe", alias="assignedToMe"),
    metadata: Json = Body(default=None),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.upload_document(
        document_name=document_name,
        file=file,
        document_type_id=document_type_id,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsing_features,
        needs_unifier=needs_unifier,
        needs_extraction=needs_extraction,
        assign_to_me=assign_to_me,
        metadata=metadata if metadata else None,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "/import",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=None,
    deprecated=True,
    description="[Deprecated] Use POST /api/v6/documents/import with mandatory documentType instead.",
)
@inject
async def import_documents(
    paths: list[str],
    source: str = Body(...),
    document_type_id: Optional[str] = Body(default=None, validation_alias="documentType", alias="documentType"),
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
    logger.warning(V5_DOCUMENT_CREATE_IMPORT_DEPRECATION_WARNING)

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
    "/{documentId}/validate",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=None,
)
@inject
async def validate_document(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.validate_document(document_id=document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "/{documentId}/pipelines/retry",
    status_code=status.HTTP_202_ACCEPTED,
    response_class=Response,
    response_model=None,
    description="Retries last failed document processing step",
)
@inject
async def retry_last_failed_step(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.retry_last_failed_step(document_id=document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "/{documentId}/pipelines/reprocess",
    status_code=status.HTTP_202_ACCEPTED,
    response_class=Response,
    response_model=None,
    description="Starts the document processing from the first step - unification",
)
@inject
async def run_from_first_step(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.run_from_first_step(document_id=document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "/pipelines/from-step",
    status_code=status.HTTP_202_ACCEPTED,
    response_class=Response,
    response_model=None,
    description="Starts the document processing from the step passed in request",
)
@inject
async def run_from_step(
    step: Status = Body(...),
    document_ids: list[str] = Body(..., validation_alias="documentIds", alias="documentIds"),
    engine: Optional[str] = Body(None, validation_alias="engineName", alias="engineName"),
    language: Optional[str] = Body(None),
    llm_type: Optional[str] = Body(None, validation_alias="llmType", alias="llmType"),
    parsing_features: Optional[list[ParsingFeature]] = Body(
        default=[], validation_alias="parsingFeatures", alias="parsingFeatures"
    ),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.run_pipeline_from_step(
        document_ids=document_ids,
        step=step,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=set(parsing_features),
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "/{documentId}/review/start",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=list[SerializedDocument],
)
@inject
async def start_review(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.start_review(document_id=document_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@documents_router.post(
    "/{documentId}/review/complete",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=SerializedDocument,
)
@inject
async def complete_review(
    document_id: str = Path(..., alias="documentId"),
    application: DocumentService = Depends(Provide[Application.document]),
) -> Response:
    proxy_response = await application.complete_review(document_id=document_id)

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
    deprecated=True,
    description="[Deprecated] Use POST /api/v6/documents with mandatory documentType instead.",
)
@inject
async def create_document(
    document_name: str = Body(..., validation_alias="documentName", alias="documentName"),
    document_type_id: Optional[str] = Body(default=None, validation_alias="documentType", alias="documentType"),
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
    logger.warning(V5_DOCUMENT_CREATE_IMPORT_DEPRECATION_WARNING)

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
