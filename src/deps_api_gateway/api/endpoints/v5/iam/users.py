from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Response, status

from deps_api_gateway.application import IAMService
from deps_api_gateway.containers import Application

from ....serializers.v5 import CreateUserRequest, SerializedExpandedUser, SerializedUser
from ....utilities import ResponseBuilder

__all__ = ["users_router"]

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("", status_code=status.HTTP_201_CREATED, response_model=SerializedUser)
@inject
async def create_user(
    user: CreateUserRequest,
    create_api_key: bool = Body(default=False, validation_alias="createAPIKey", alias="createAPIKey"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.create_user(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        organisation=user.organisation,
        create_api_key=create_api_key,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@users_router.get("/me", status_code=status.HTTP_200_OK, response_model=SerializedExpandedUser)
@inject
async def get_current_user(
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_current_user()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@users_router.get(
    "/me/api-key",
    status_code=status.HTTP_200_OK,
    response_model=str,
    summary="Get user's API key. If it does not exist generate a new one",
)
@inject
async def get_or_create_user_api_key(
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_or_create_user_api_key()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@users_router.delete(
    "/me/api-key",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Revoke user's api key",
)
@inject
async def revoke_user_api_key(
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.revoke_user_api_key()

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@users_router.get("/{userId}", status_code=status.HTTP_200_OK, response_model=SerializedUser)
@inject
async def get_user(
    user_id: str = Path(..., alias="userId"),
    application: IAMService = Depends(Provide[Application.iam]),
) -> Response:
    proxy_response = await application.get_user(user_id)

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
