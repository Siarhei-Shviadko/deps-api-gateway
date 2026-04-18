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

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    AddMarkupRequest,
    CreateTemplateRequest,
    CreateTemplateResponse,
    SerializedTemplateVersion,
    TemplateVersionsList,
    UpdateTemplateVersionRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["template_router"]

template_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Template Extractors"])


@template_router.post(
    "/template",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTemplateResponse,
    description="Create a document type with the Template extractor type. If `baseTemplateId` is provided then "
    "extraction fields from the base document type will be copied into the newly created one",
)
@inject
async def create_template(
    template_data: CreateTemplateRequest,
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_template(
        src_template_id=template_data.src_template_id,
        name=template_data.name,
        language=template_data.language,
        engine=template_data.engine,
        description=template_data.description,
        group_id=template_data.group_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@template_router.get(
    "/{documentTypeId}/template/versions",
    status_code=status.HTTP_200_OK,
    response_model=TemplateVersionsList,
)
@inject
async def get_template_versions(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_template_versions(document_type_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@template_router.get(
    "/{documentTypeId}/template/versions/{versionId}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedTemplateVersion,
)
@inject
async def get_template_version(
    document_type_id: str = Path(..., alias="documentTypeId"),
    version_id: str = Path(..., alias="versionId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_template_version(document_type_id=document_type_id, version_id=version_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@template_router.post(
    "/{documentTypeId}/template/versions",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
@inject
async def create_template_version(
    document_type_id: str = Path(..., alias="documentTypeId"),
    files: list[UploadFile] = File(...),
    name: str = Body(..., min_length=1),
    description: Optional[str] = Body(default=None, max_length=100),
    markup_automatically: bool = Body(default=False, alias="markupAutomatically"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_template_version(
        document_type_id=document_type_id,
        files=files,
        name=name,
        description=description,
        markup_automatically=markup_automatically,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@template_router.patch(
    "/{documentTypeId}/template/versions/{versionId}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedTemplateVersion,
)
@inject
async def update_template_version(
    version_data: UpdateTemplateVersionRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    version_id: str = Path(..., alias="versionId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_template_version(
        document_type_id=document_type_id, version_id=version_id, name=version_data.name
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@template_router.delete(
    "/{documentTypeId}/template/versions",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def delete_template_versions(
    document_type_id: str = Path(..., alias="documentTypeId"),
    version_ids: list[str] = Query(..., alias="ids"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_template_versions(
        document_type_id=document_type_id, version_ids=version_ids
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@template_router.put(
    "/{documentTypeId}/template/versions/{versionId}/markups",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
@inject
async def add_markup(
    markup_data: AddMarkupRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    version_id: str = Path(..., alias="versionId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.add_markup(
        document_type_id=document_type_id,
        version_id=version_id,
        reference_page=markup_data.reference_page,
        markups=markup_data.markups,
        markup_types=markup_data.markup_types,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
