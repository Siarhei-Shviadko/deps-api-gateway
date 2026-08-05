import json
from typing import Any, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Path, Query, Response, UploadFile
from fastapi import status as http_status

from deps_api_gateway.api.serializers.v5.file import (
    CreateBatchFromFileRequest,
    CreateDocumentFromFileRequest,
    CreateFileResponse,
    GetFilesRequest,
    SerializedFileInfo,
)
from deps_api_gateway.api.utilities import ResponseBuilder
from deps_api_gateway.application.file.service import FileService
from deps_api_gateway.application.parsing import ParsingType
from deps_api_gateway.constants import FILES_ROUTER_PREFIX
from deps_api_gateway.containers import Application
from deps_api_gateway.domain.exceptions import IllegalArgument

__all__ = ["file_router"]

file_router = APIRouter(prefix=FILES_ROUTER_PREFIX, tags=["Files"])


def parse_json_str(value: str | None, field_name: str) -> Any:
    if value is None or value == "":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise IllegalArgument(f"Invalid JSON in field '{field_name}'. {str(e)}")


@file_router.get(
    "",
    status_code=http_status.HTTP_200_OK,
    response_model=SerializedFileInfo,
)
@inject
async def list_files(
    state: list[str] = Query(default=None),
    get_files_request: GetFilesRequest = Depends(),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.get_files(
        name=get_files_request.name,
        state=state,
        labels=get_files_request.labels,
        date_start=get_files_request.date_start,
        date_end=get_files_request.date_end,
        page=get_files_request.page,
        per_page=get_files_request.per_page,
        sort_by=get_files_request.sort_by,
        sort_order=get_files_request.sort_order,
        reference_available=get_files_request.reference_available,
        reference=get_files_request.reference,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.get(
    "/{file_id}",
    status_code=http_status.HTTP_200_OK,
    response_model=SerializedFileInfo,
)
@inject
async def get_file(
    file_id: str,
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.get_file(file_id=file_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.post(
    "/process",
    status_code=http_status.HTTP_201_CREATED,
    response_model=CreateFileResponse,
)
@inject
async def process_file(
    file: UploadFile = File(...),
    engine: str | None = Body(ParsingType.TESSERACT),
    language: str | None = Body(None),
    llm_type: str | None = Body(None, validation_alias="llmType", alias="llmType"),
    parsing_features: Optional[str] = Body(
        None,
        validation_alias="parsingFeatures",
        alias="parsingFeatures",
        description=(
            r'Parsing features as JSON string. Swagger format: "[\\"text\\", \\"images\\"]". '
            'REST API format: ["text", "images"]'
        ),
    ),
    needs_unifier: bool = Body(..., validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(..., validation_alias="needsExtraction", alias="needsExtraction"),
    assigned_to_me: bool = Body(..., validation_alias="assignedToMe", alias="assignedToMe"),
    metadata: Optional[str] = Body(
        None,
        description=r'Metadata as JSON string. Swagger format: "{\\"name\\": \\"test\\"}". REST API format: {"name": "test"}',
    ),
    labels: Optional[str] = Body(
        None,
        description=r'Labels as JSON string. Swagger format: "[\\"L1\\", \\"L2\\"]". REST API format: ["L1", "L2"]',
    ),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    parsed_parsing_features = parse_json_str(parsing_features, "parsingFeatures")
    parsed_labels = parse_json_str(labels, "labels")
    parsed_metadata = parse_json_str(metadata, "metadata")

    proxy_response = await file_service.process_file(
        file=file,
        labels=parsed_labels,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsed_parsing_features,
        needs_unifier=needs_unifier,
        needs_extraction=needs_extraction,
        assigned_to_me=assigned_to_me,
        metadata=parsed_metadata,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.post(
    "/classify",
    status_code=http_status.HTTP_201_CREATED,
    response_model=CreateFileResponse,
)
@inject
async def classify_file(
    file: UploadFile = File(...),
    engine: str | None = Body(ParsingType.TESSERACT),
    language: str | None = Body(None),
    llm_type: str | None = Body(None, validation_alias="llmType", alias="llmType"),
    parsing_features: Optional[str] = Body(
        None,
        validation_alias="parsingFeatures",
        alias="parsingFeatures",
        description=(
            r'Parsing features as JSON string. Swagger format: "[\\"text\\", \\"images\\"]". '
            'REST API format: ["text", "images"]'
        ),
    ),
    needs_unifier: bool = Body(..., validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(..., validation_alias="needsExtraction", alias="needsExtraction"),
    assigned_to_me: bool = Body(..., validation_alias="assignedToMe", alias="assignedToMe"),
    metadata: Optional[str] = Body(
        default=None,
        description=r'Metadata as JSON string. Swagger format: "{\\"name\\": \\"test\\"}". REST API format: {"name": "test"}',
    ),
    labels: Optional[str] = Body(
        None,
        description=r'Labels as JSON string. Swagger format: "[\\"L1\\", \\"L2\\"]". REST API format: ["L1", "L2"]',
    ),
    group_id: str = Body(..., validation_alias="groupId", alias="groupId"),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    parsed_parsing_features = parse_json_str(parsing_features, "parsingFeatures")
    parsed_labels = parse_json_str(labels, "labels")
    parsed_metadata = parse_json_str(metadata, "metadata")

    proxy_response = await file_service.classify_file(
        file=file,
        group_id=group_id,
        labels=parsed_labels,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsed_parsing_features,
        needs_unifier=needs_unifier,
        needs_extraction=needs_extraction,
        assigned_to_me=assigned_to_me,
        metadata=parsed_metadata,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.patch(
    "/{file_id}/classify",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
@inject
async def classify_existing_file(
    file_id: str,
    engine: str | None = Body(None),
    language: str | None = Body(None),
    llm_type: str | None = Body(None, validation_alias="llmType", alias="llmType"),
    parsing_features: list[str] | None = Body(None, validation_alias="parsingFeatures", alias="parsingFeatures"),
    needs_unifier: bool = Body(..., validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(..., validation_alias="needsExtraction", alias="needsExtraction"),
    assigned_to_me: bool = Body(..., validation_alias="assignedToMe", alias="assignedToMe"),
    metadata: dict[str, Any] | None = Body(default=None),
    group_id: str = Body(..., validation_alias="groupId", alias="groupId"),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.classify_existing_file(
        file_id=file_id,
        group_id=group_id,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsing_features,
        needs_unifier=needs_unifier,
        needs_extraction=needs_extraction,
        assigned_to_me=assigned_to_me,
        metadata=metadata,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.post(
    "/split",
    status_code=http_status.HTTP_201_CREATED,
    response_model=CreateFileResponse,
)
@inject
async def split_file(
    file: UploadFile = File(...),
    document_type_id: str | None = Body(None, validation_alias="documentTypeId", alias="documentTypeId"),
    classification_enabled: bool = Body(..., validation_alias="classificationEnabled", alias="classificationEnabled"),
    engine: str | None = Body(ParsingType.TESSERACT),
    language: str | None = Body(None),
    llm_type: str | None = Body(None, validation_alias="llmType", alias="llmType"),
    parsing_features: Optional[str] = Body(
        None,
        validation_alias="parsingFeatures",
        alias="parsingFeatures",
        description=(
            r'Parsing features as JSON string. Swagger format: "[\\"text\\", \\"images\\"]". '
            'REST API format: ["text", "images"]'
        ),
    ),
    needs_unifier: bool = Body(..., validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(..., validation_alias="needsExtraction", alias="needsExtraction"),
    assigned_to_me: bool = Body(..., validation_alias="assignedToMe", alias="assignedToMe"),
    needs_splitting_proposal_review: bool = Body(
        default=False,
        validation_alias="needsSplittingProposalReview",
        alias="needsSplittingProposalReview",
    ),
    metadata: Optional[str] = Body(
        default=None,
        description=r'Metadata as JSON string. Swagger format: "{\\"name\\": \\"test\\"}". REST API format: {"name": "test"}',
    ),
    labels: Optional[str] = Body(
        None,
        description=r'Labels as JSON string. Swagger format: "[\\"L1\\", \\"L2\\"]". REST API format: ["L1", "L2"]',
    ),
    group_id: str = Body(..., validation_alias="groupId", alias="groupId"),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    parsed_parsing_features = parse_json_str(parsing_features, "parsingFeatures")
    parsed_labels = parse_json_str(labels, "labels")
    parsed_metadata = parse_json_str(metadata, "metadata")

    proxy_response = await file_service.split_file(
        file=file,
        document_type_id=document_type_id,
        classification_enabled=classification_enabled,
        group_id=group_id,
        labels=parsed_labels,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsed_parsing_features,
        needs_unifier=needs_unifier,
        needs_extraction=needs_extraction,
        assigned_to_me=assigned_to_me,
        needs_splitting_proposal_review=needs_splitting_proposal_review,
        metadata=parsed_metadata,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.patch(
    "/{fileId}/split",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
@inject
async def split_existing_file(
    file_id: str = Path(..., validation_alias="fileId", alias="fileId"),
    document_type_id: str | None = Body(None, validation_alias="documentTypeId", alias="documentTypeId"),
    classification_enabled: bool = Body(..., validation_alias="classificationEnabled", alias="classificationEnabled"),
    engine: str | None = Body(None),
    language: str | None = Body(None),
    llm_type: str | None = Body(None, validation_alias="llmType", alias="llmType"),
    parsing_features: list[str] | None = Body(None, validation_alias="parsingFeatures", alias="parsingFeatures"),
    needs_unifier: bool = Body(..., validation_alias="needsUnifier", alias="needsUnifier"),
    needs_extraction: bool = Body(..., validation_alias="needsExtraction", alias="needsExtraction"),
    assigned_to_me: bool = Body(..., validation_alias="assignedToMe", alias="assignedToMe"),
    needs_splitting_proposal_review: bool = Body(
        default=False,
        validation_alias="needsSplittingProposalReview",
        alias="needsSplittingProposalReview",
    ),
    metadata: dict[str, Any] | None = Body(default=None),
    group_id: str = Body(..., validation_alias="groupId", alias="groupId"),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.split_existing_file(
        file_id=file_id,
        document_type_id=document_type_id,
        classification_enabled=classification_enabled,
        group_id=group_id,
        engine=engine,
        language=language,
        llm_type=llm_type,
        parsing_features=parsing_features,
        needs_unifier=needs_unifier,
        needs_extraction=needs_extraction,
        assigned_to_me=assigned_to_me,
        needs_splitting_proposal_review=needs_splitting_proposal_review,
        metadata=metadata,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.delete(
    "",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_files(
    ids: list[str] = Query(...),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.delete_files(ids=ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.post(
    "/{fileId}/create-document",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
@inject
async def create_document_from_file(
    file_id: str = Path(..., validation_alias="fileId", alias="fileId"),
    data_request: CreateDocumentFromFileRequest = Body(...),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.create_document_from_file(
        file_id=file_id,
        document_type_id=data_request.document_type_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.post(
    "/{fileId}/create-batch",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
@inject
async def create_batch_from_file(
    file_id: str = Path(..., validation_alias="fileId", alias="fileId"),
    data_request: CreateBatchFromFileRequest = Body(...),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.create_batch_from_file(
        file_id=file_id,
        batch_name=data_request.batch_name,
        batch_files=data_request.batch_files,
        group_id=data_request.group_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@file_router.post(
    "/{fileId}/restart",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
@inject
async def restart_file(
    file_id: str = Path(..., validation_alias="fileId", alias="fileId"),
    file_service: FileService = Depends(Provide[Application.file]),
) -> Response:
    proxy_response = await file_service.restart_file(file_id=file_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
