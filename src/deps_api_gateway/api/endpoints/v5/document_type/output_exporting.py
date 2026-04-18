from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application
from deps_api_gateway.domain import ProfileData

from ....serializers.v5.output_exporting import (
    CreateProfileRequest,
    SaveProfileResponse,
    UpdateProfileRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["output_exporting_router"]


output_exporting_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Output Exporting"])


@output_exporting_router.post(
    "/{documentTypeId}/profiles",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
    response_model=SaveProfileResponse,
)
@inject
async def save_profiles(
    request: CreateProfileRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    storages = (
        [storage.model_dump(by_alias=True) for storage in request.external_storages_info]
        if request.external_storages_info
        else None
    )
    profile = ProfileData(
        name=request.name,
        schema=request.schema_.model_dump(by_alias=True),
        format=request.format,
        external_storages_info=storages,
    )
    proxy_response = await application.save_profile(document_type_id=document_type_id, profile=profile)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@output_exporting_router.put(
    "/{documentTypeId}/profiles/{profileId}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=SaveProfileResponse,
)
@inject
async def update_profile(
    request: UpdateProfileRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    profile_id: str = Path(..., alias="profileId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    storages = (
        [storage.model_dump(by_alias=True) for storage in request.external_storages_info]
        if request.external_storages_info
        else None
    )
    profile = ProfileData(
        name=request.name,
        schema=request.schema_.model_dump(by_alias=True),
        format=None,
        external_storages_info=storages,
    )
    proxy_response = await application.update_profile(
        document_type_id=document_type_id,
        profile_id=profile_id,
        profile=profile,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@output_exporting_router.delete(
    "/{documentTypeId}/profiles/{profileId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
@inject
async def delete_profile(
    document_type_id: str = Path(..., alias="documentTypeId"),
    profile_id: str = Path(..., alias="profileId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_profile(document_type_id=document_type_id, profile_id=profile_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
