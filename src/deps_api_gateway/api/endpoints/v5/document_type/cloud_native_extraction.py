from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    AzureExtractorHealthcheckResponse,
    AzureExtractorInfoResponse,
    CreateAzureExtractorRequest,
    CreateAzureExtractorRespose,
    UpdateAzureExtractorRequest,
    ValidateAzureCredentialsRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["cloud_native_extraction_router"]

cloud_native_extraction_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Azure Cloud Native Extractors"])


@cloud_native_extraction_router.post(
    "/azure-extractor",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateAzureExtractorRespose,
)
@inject
async def create_azure_extractor(
    extractor_request: CreateAzureExtractorRequest,
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_azure_extractor(
        name=extractor_request.name,
        model_id=extractor_request.model_id,
        endpoint=extractor_request.endpoint,
        api_key=extractor_request.api_key,
        language=extractor_request.language,
        description=extractor_request.description,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@cloud_native_extraction_router.get(
    "/{documentTypeId}/azure-extractor",
    status_code=status.HTTP_200_OK,
    response_model=AzureExtractorInfoResponse,
)
@inject
async def get_azure_extractor_info(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_azure_extractor_info(document_type_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@cloud_native_extraction_router.post(
    "/azure-extractor/validate-credentials",
    status_code=status.HTTP_200_OK,
    response_model=AzureExtractorInfoResponse,
)
@inject
async def validate_azure_extractor_credentials(
    credentials: ValidateAzureCredentialsRequest,
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.validate_azure_credentials(
        endpoint=credentials.endpoint,
        model_id=credentials.model_id,
        api_key=credentials.api_key,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@cloud_native_extraction_router.put(
    "/{documentTypeId}/azure-extractor",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def update_azure_extractor(
    update_azure_extractor_data: UpdateAzureExtractorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_azure_extractor(
        document_type_id=document_type_id,
        endpoint=update_azure_extractor_data.endpoint,
        model_id=update_azure_extractor_data.model_id,
        api_key=update_azure_extractor_data.api_key,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@cloud_native_extraction_router.get(
    "/{documentTypeId}/azure-extractor/checkup",
    status_code=status.HTTP_200_OK,
    response_model=AzureExtractorHealthcheckResponse,
)
@inject
async def azure_extractor_healthcheck(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.azure_extractor_checkup(document_type_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@cloud_native_extraction_router.put(
    "/{documentTypeId}/azure-extractor/synchronize",
    status_code=status.HTTP_200_OK,
    response_model=AzureExtractorHealthcheckResponse,
)
@inject
async def synchronize_azure_extractor(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.synchronize_azure_extractor(document_type_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
