from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query, Response, status

from deps_api_gateway.application import (
    IAMService,
    InvitationSortingField,
    UserSortingField,
)
from deps_api_gateway.containers import Application

from ....serializers.v5 import (
    ApproveUserResponse,
    DeclineUserRequest,
    DeleteUserResponse,
    GetOrganisationInviteesResponse,
    GetOrganisationsResponse,
    GetOrganisationUsersResponse,
    SerializedExpandedUser,
    SerializedInvitation,
    SerializedOrganisation,
)
from ....utilities import ResponseBuilder

__all__ = ["organisation_router"]


organisation_router = APIRouter(prefix="/organisations", tags=["Organisations"])


@organisation_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=GetOrganisationsResponse,
    summary="Get all organisations the user is a member of",
)
@inject
async def get_organisations(
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_user_organisations()
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.get(
    "/{organisationId}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedOrganisation,
)
@inject
async def get_organisation_detail(
    organisation_id: str = Path(..., alias="organisationId"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_organisation_detail(organisation_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.get(
    "/{organisationId}/users",
    status_code=status.HTTP_200_OK,
    response_model=GetOrganisationUsersResponse,
)
@inject
async def get_organisation_users(
    organisation_id: str = Path(..., alias="organisationId"),
    page: int = Query(1),
    per_page: int = Query(10, ge=1, alias="perPage"),
    full_name: Optional[str] = Query(
        None,
        alias="fullName",
        description="Search by first and last names",
    ),
    sort_by: Optional[UserSortingField] = Query(None, alias="sortBy"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_organisation_users(
        organisation_id=organisation_id,
        page=page,
        per_page=per_page,
        full_name=full_name,
        sort_by=sort_by,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.get(
    "/{organisationId}/invitees",
    status_code=status.HTTP_200_OK,
    response_model=GetOrganisationInviteesResponse,
)
@inject
async def get_organisation_invitees(
    organisation_id: str = Path(..., alias="organisationId"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, alias="perPage"),
    email: Optional[str] = Query(
        None,
        alias="email",
        description="Search by email",
    ),
    sort_by: InvitationSortingField = Query(InvitationSortingField.EMAIL_DESC, alias="sortBy"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_organisation_invitees(
        organisation_id=organisation_id,
        page=page,
        per_page=per_page,
        email=email,
        sort_by=sort_by,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.get(
    "/{organisationId}/approvals",
    status_code=status.HTTP_200_OK,
    response_model=GetOrganisationUsersResponse,
)
@inject
async def get_organisation_approvals(
    organisation_id: str = Path(..., alias="organisationId"),
    page: int = Query(1),
    per_page: int = Query(10, ge=1, alias="perPage"),
    full_name: Optional[str] = Query(
        None,
        alias="fullName",
        description="Search by first and last names",
    ),
    sort_by: Optional[UserSortingField] = Query(None, alias="sortBy"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_organisation_approvals(
        organisation_id=organisation_id,
        page=page,
        per_page=per_page,
        full_name=full_name,
        sort_by=sort_by,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.post("", status_code=status.HTTP_201_CREATED, response_model=SerializedOrganisation)
@inject
async def create_organisation(
    name: str = Body(...),
    organisation_id: Optional[str] = Body(None, validation_alias="organisationId", alias="organisationId"),
    customization_url: Optional[str] = Body(None, validation_alias="customizationUrl", alias="customizationUrl"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.create_organisation(
        organisation_id=organisation_id,
        name=name,
        customization_url=customization_url,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.post(
    "/{organisationId}/activate",
    status_code=status.HTTP_200_OK,
    response_model=SerializedOrganisation,
    summary="Activate the specified user's organisation. This enables access to documents and document types "
    + "associated with the organisation.",
)
@inject
async def activate_user_organisation(
    organisation_id: str = Path(..., alias="organisationId"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.activate_user_organisation(organisation_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.post(
    "/{organisationId}/invite",
    status_code=status.HTTP_200_OK,
    response_model=SerializedInvitation,
    summary="Send invitations to a list of emails. Existing users are added to the organisation, "
    + "while non-users receive an invitation email.",
)
@inject
async def invite_users_to_organisation(
    invitations: list[SerializedInvitation],
    organisation_id: str = Path(..., alias="organisationId"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.invite_user_to_organisation(
        organisation_id=organisation_id,
        emails=[invite.email for invite in invitations],
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.post(
    "/{organisationId}/join",
    status_code=status.HTTP_200_OK,
    response_model=SerializedExpandedUser,
    summary="Join an organisation if the user invited to the organisation."
    + " Otherwise, an approval request is created.",
)
@inject
async def join_organisation(
    organisation_id: str = Path(..., alias="organisationId"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.join_organisation(organisation_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.post(
    "/{organisationId}/approve",
    status_code=status.HTTP_200_OK,
    response_model=ApproveUserResponse,
    summary="Approve user requests to join an organisation. Once approved, "
    + "the organisation becomes active for the users.",
)
@inject
async def approve_user_requests(
    organisation_id: str = Path(..., alias="organisationId"),
    user_ids: list[str] = Body(..., validation_alias="userIds", alias="userIds", min_length=1, embed=True),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.approve_user_requests(organisation_id=organisation_id, user_ids=user_ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.patch(
    "/{organisationId}",
    status_code=status.HTTP_200_OK,
    response_model=SerializedOrganisation,
)
@inject
async def update_organisation(
    organisation_id: str = Path(..., alias="organisationId"),
    name: Optional[str] = Body(None),
    customization_url: Optional[str] = Body(None, validation_alias="customizationUrl", alias="customizationUrl"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.update_organisation(
        organisation_id=organisation_id,
        name=name,
        customization_url=customization_url,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.delete(
    "/{organisationId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_organization(
    organisation_id: str = Path(..., alias="organisationId"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.delete_organisation(organisation_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.delete(
    "/{organisationId}/approvals",
    status_code=status.HTTP_200_OK,
    response_model=DeclineUserRequest,
    summary="Decline and remove pending user requests to join the organisation.",
)
@inject
async def decline_user_requests(
    organisation_id: str = Path(..., alias="organisationId"),
    user_ids: list[str] = Body(..., validation_alias="userIds", alias="userIds", min_length=1, embed=True),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.decline_user_requests(organisation_id=organisation_id, user_ids=user_ids)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.delete(
    "/{organisationId}/invitees",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Remove invited users from the organisation who hasn't accepted the invitation yet.",
)
@inject
async def delete_invitees_from_organisation(
    organisation_id: str = Path(..., alias="organisationId"),
    invitees: list[str] = Body(..., embed=True),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.delete_invitees_from_organisation(
        organisation_id=organisation_id, invitees=invitees
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@organisation_router.delete(
    "/{organisationId}/users",
    status_code=status.HTTP_200_OK,
    response_model=DeleteUserResponse,
    summary="Permanently remove specified users from the organisation.",
)
@inject
async def delete_users_from_organisation(
    organisation_id: str = Path(..., alias="organisationId"),
    user_ids: list[str] = Body(..., alias="userIds", min_length=1, embed=True),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.delete_users_from_organisation(
        organisation_id=organisation_id, user_ids=user_ids
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
