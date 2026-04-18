from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IIAMProxy,
    InvitationSortingField,
    ProxyResponse,
    ProxyResponseFactory,
    UserSortingField,
)
from deps_api_gateway.constants import IAM_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import IAMServiceUnavailableError

__all__ = ["IAMProxy"]


class IAMProxy(GenericRestClient, IIAMProxy):
    exception = IAMServiceUnavailableError
    v1_prefix = f"{IAM_BASE_API_PREFIX}{V1_PREFIX}"
    organisation_resource = f"{v1_prefix}/organisations"
    user_resource = f"{v1_prefix}/users"

    async def activate_user_organisation(self, organisation_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=f"{self.organisation_resource}/{organisation_id}/activate")
            )

    async def invite_user_to_organisation(self, organisation_id: str, emails: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.organisation_resource}/{organisation_id}/invite",
                    json=[{"email": email} for email in emails],
                )
            )

    async def join_organisation(self, organisation_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.organisation_resource}/{organisation_id}/join",
                )
            )

    async def approve_user_requests(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.organisation_resource}/{organisation_id}/approve",
                    json={"userPks": user_ids},
                )
            )

    async def delete_approvals(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.organisation_resource}/{organisation_id}/approvals",
                    json={"userPks": user_ids},
                )
            )

    async def delete_users_from_organisation(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.organisation_resource}/{organisation_id}/users",
                    json={"users": user_ids},
                )
            )

    async def delete_invitees_from_organisation(self, organisation_id: str, invitees: list[str]) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.organisation_resource}/{organisation_id}/invitees",
                    json={"invitees": invitees},
                )
            )

    async def create_user(
        self,
        email: str,
        username: Optional[str] = None,
        first_name: Optional[str] = "",
        last_name: Optional[str] = "",
        organisation: Optional[str] = None,
        create_api_key: bool = False,
    ) -> ProxyResponse:
        user = {
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
        }
        if username is not None:
            user["username"] = username
        if organisation is not None:
            user["organisation"] = organisation

        data = {
            "user": user,
            "createAPIKey": create_api_key,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=f"{self.user_resource}", json=data)
            )

    async def get_current_user(self) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.user_resource}/me")
            )

    async def get_user_api_key(self) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.user_resource}/me/api-key")
            )

    async def generate_user_api_key(self) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=f"{self.user_resource}/me/api-key/generate")
            )

    async def revoke_user_api_key(self) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=f"{self.user_resource}/me/api-key")
            )

    async def get_user_organisations(self) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.organisation_resource}")
            )

    async def get_organisation_detail(self, organisation_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.organisation_resource}/{organisation_id}")
            )

    async def get_organisation_users(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        full_name: Optional[str] = None,
        sort_by: Optional[UserSortingField] = None,
    ) -> ProxyResponse:
        data: dict = {
            "page": page,
            "perPage": per_page,
        }
        if full_name is not None:
            data["firstName_lastName"] = full_name
        if sort_by is not None:
            data["sortBy"] = sort_by.value

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.organisation_resource}/{organisation_id}/users",
                    params=data,
                )
            )

    async def get_organisation_invitees(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        email: Optional[str] = None,
        sort_by: Optional[InvitationSortingField] = None,
    ) -> ProxyResponse:
        data: dict = {
            "page": page,
            "perPage": per_page,
        }
        if email is not None:
            data["email"] = email
        if sort_by is not None:
            data["sortBy"] = sort_by.value

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.organisation_resource}/{organisation_id}/invitees",
                    params=data,
                )
            )

    async def get_organisation_approvals(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        full_name: Optional[str] = None,
        sort_by: Optional[UserSortingField] = None,
    ) -> ProxyResponse:
        data: dict = {
            "page": page,
            "perPage": per_page,
        }
        if full_name is not None:
            data["firstName_lastName"] = full_name
        if sort_by is not None:
            data["sortBy"] = sort_by.value

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.organisation_resource}/{organisation_id}/approvals",
                    params=data,
                )
            )

    async def create_organisation(
        self,
        organisation_id: Optional[str],
        name: str,
        customization_url: Optional[str] = None,
    ) -> ProxyResponse:
        data = {"name": name}
        if organisation_id is not None:
            data["pk"] = organisation_id
        if customization_url is not None:
            data["customizationUrl"] = customization_url

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=f"{self.organisation_resource}", json=data)
            )

    async def delete_organisation(self, organisation_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=f"{self.organisation_resource}/{organisation_id}")
            )

    async def update_organisation(
        self,
        organisation_id: str,
        name: Optional[str],
        customization_url: Optional[str],
    ) -> ProxyResponse:
        data = {}
        if name is not None:
            data["name"] = name
        if customization_url is not None:
            data["customizationUrl"] = customization_url

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH, url=f"{self.organisation_resource}/{organisation_id}", json=data
                )
            )

    async def get_user(self, user_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.user_resource}/{user_id}")
            )
