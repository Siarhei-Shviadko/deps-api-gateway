from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Query, Response, status

from deps_api_gateway.application import GetGroupExtras, GroupService
from deps_api_gateway.constants import GROUPS_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    AddDocumentTypesRequest,
    CreateGenAIClassifierRequest,
    CreateGenAIClassifierResponse,
    CreateGroupRequest,
    CreateGroupResponse,
    GetClassifiersOfGroupResponse,
    GetGroupResponse,
    GetGroupsRequest,
    GetGroupsResponse,
    UpdateGenAIClassifierRequest,
    UpdateGroupInfoRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["groups_router"]


groups_router = APIRouter(prefix=GROUPS_ROUTER_PREFIX, tags=["Document Type Groups"])


@groups_router.get("", status_code=status.HTTP_200_OK, response_model=GetGroupsResponse)
@inject
async def get_groups(
    get_groups_request: GetGroupsRequest = Depends(),
    group_service: GroupService = Depends(Provide[Application.group]),
) -> Response:
    proxy_response = await group_service.get_groups(
        name=get_groups_request.name,
        document_type_id=get_groups_request.document_type_id,
        date_start=get_groups_request.date_start,
        date_end=get_groups_request.date_end,
        page=get_groups_request.page,
        per_page=get_groups_request.per_page,
        sort_by=get_groups_request.sort_by,
        sort_order=get_groups_request.sort_order,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateGroupResponse,
)
@inject
async def create_group(
    create_group_request: CreateGroupRequest,
    group_service: GroupService = Depends(Provide[Application.group]),
):
    proxy_response = await group_service.create_group(
        name=create_group_request.name,
        document_type_ids=create_group_request.document_type_ids,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_groups(
    ids: list[str] = Query(..., alias="id"),
    group_service: GroupService = Depends(Provide[Application.group]),
):
    proxy_response = await group_service.delete_groups(
        ids=ids,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.get(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetGroupResponse,
)
@inject
async def get_group(
    group_id: str,
    extras: Optional[list[GetGroupExtras]] = Query(None),
    group_service: GroupService = Depends(Provide[Application.group]),
):
    proxy_response = await group_service.get_group(group_id=group_id, extras=extras)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.patch(
    "/{group_id}/document-types",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def add_document_types(
    group_id: str,
    add_document_types_request: AddDocumentTypesRequest,
    group_service: GroupService = Depends(Provide[Application.group]),
):
    proxy_response = await group_service.add_document_types(
        group_id=group_id,
        document_type_ids=add_document_types_request.document_type_ids,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.delete(
    "/{group_id}/document-types",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def remove_document_types(
    group_id: str,
    document_type_ids: list[str] = Query(..., alias="id"),
    group_service: GroupService = Depends(Provide[Application.group]),
):
    proxy_response = await group_service.remove_document_types(
        group_id=group_id,
        document_type_ids=document_type_ids,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.patch(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def update_group_info(
    group_id: str,
    update_group_info_request: UpdateGroupInfoRequest,
    group_service: GroupService = Depends(Provide[Application.group]),
):
    proxy_response = await group_service.update_group_info(
        group_id=group_id,
        name=update_group_info_request.name,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.post(
    "/{groupId}/document-types/{documentTypeId}/gen-ai-classifiers",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateGenAIClassifierResponse,
)
@inject
async def create_gen_ai_classifier(
    create_gen_ai_classifier_request: CreateGenAIClassifierRequest,
    group_id: str = Path(..., alias="groupId"),
    document_type_id: str = Path(..., alias="documentTypeId"),
    group_service: GroupService = Depends(Provide[Application.group]),
) -> Response:
    proxy_response = await group_service.create_gen_ai_classifier(
        group_id=group_id,
        document_type_id=document_type_id,
        prompt=create_gen_ai_classifier_request.prompt,
        llm_type=create_gen_ai_classifier_request.llm_type,
        name=create_gen_ai_classifier_request.name,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.patch(
    "/gen-ai-classifiers/{genAIClassifierId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
@inject
async def update_gen_ai_classifier(
    update_gen_ai_classifier_request: UpdateGenAIClassifierRequest,
    gen_ai_classifier_id: str = Path(..., alias="genAIClassifierId"),
    group_service: GroupService = Depends(Provide[Application.group]),
) -> Response:
    proxy_response = await group_service.update_gen_ai_classifier(
        gen_ai_classifier_id=gen_ai_classifier_id,
        prompt=update_gen_ai_classifier_request.prompt,
        llm_type=update_gen_ai_classifier_request.llm_type,
        name=update_gen_ai_classifier_request.name,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.delete("/gen-ai-classifiers", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
@inject
async def delete_gen_ai_classifiers(
    ids: list[str] = Query(..., alias="id"),
    group_service: GroupService = Depends(Provide[Application.group]),
) -> Response:
    proxy_response = await group_service.delete_gen_ai_classifiers(ids=ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@groups_router.get(
    "/{groupId}/classifiers", status_code=status.HTTP_200_OK, response_model=GetClassifiersOfGroupResponse
)
@inject
async def get_classifiers_of_group(
    group_id: str = Path(..., alias="groupId"),
    group_service: GroupService = Depends(Provide[Application.group]),
) -> Response:
    proxy_response = await group_service.get_classifiers_of_group(group_id=group_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
