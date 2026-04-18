from http import HTTPStatus
from typing import Optional

from ..iproxies import IIAMProxy
from ..proxy_response import ProxyResponse
from ..types import InvitationSortingField, UserSortingField
from .consolidator import IAMConsolidator

__all__ = ["IAMService"]


class IAMService:
    def __init__(
        self,
        proxy: IIAMProxy,
    ) -> None:
        self._proxy = proxy

    async def activate_user_organisation(self, organisation_id: str) -> ProxyResponse:
        return await self._proxy.activate_user_organisation(organisation_id)

    async def invite_user_to_organisation(self, organisation_id: str, emails: list[str]) -> ProxyResponse:
        return await self._proxy.invite_user_to_organisation(organisation_id=organisation_id, emails=emails)

    async def join_organisation(self, organisation_id: str) -> ProxyResponse:
        return await self._proxy.join_organisation(organisation_id)

    async def approve_user_requests(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        return await self._proxy.approve_user_requests(organisation_id=organisation_id, user_ids=user_ids)

    async def decline_user_requests(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        return await self._proxy.delete_approvals(organisation_id=organisation_id, user_ids=user_ids)

    async def delete_users_from_organisation(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        return await self._proxy.delete_users_from_organisation(organisation_id=organisation_id, user_ids=user_ids)

    async def delete_invitees_from_organisation(self, organisation_id: str, invitees: list[str]) -> ProxyResponse:
        return await self._proxy.delete_invitees_from_organisation(organisation_id=organisation_id, invitees=invitees)

    async def create_user(
        self,
        email: str,
        username: Optional[str] = None,
        first_name: Optional[str] = "",
        last_name: Optional[str] = "",
        organisation: Optional[str] = None,
        create_api_key: bool = False,
    ) -> ProxyResponse:
        return await self._proxy.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            organisation=organisation,
            create_api_key=create_api_key,
        )

    async def get_current_user(self) -> ProxyResponse:
        return await self._proxy.get_current_user()

    async def get_or_create_user_api_key(self) -> ProxyResponse:
        response = await self._proxy.get_user_api_key()

        if response.status_code == HTTPStatus.NOT_FOUND:
            response = await self._proxy.generate_user_api_key()

            if response.status_code == HTTPStatus.CREATED:
                response.status_code = HTTPStatus.OK

        return response

    async def revoke_user_api_key(self) -> ProxyResponse:
        return await self._proxy.revoke_user_api_key()

    async def get_user_organisations(self) -> ProxyResponse:
        return IAMConsolidator.consolidate_organisations_list(await self._proxy.get_user_organisations())

    async def get_organisation_detail(self, organisation_id: str) -> ProxyResponse:
        return await self._proxy.get_organisation_detail(organisation_id)

    async def get_organisation_users(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        full_name: Optional[str] = None,
        sort_by: Optional[UserSortingField] = None,
    ) -> ProxyResponse:
        return await self._proxy.get_organisation_users(
            organisation_id=organisation_id,
            page=page,
            per_page=per_page,
            full_name=full_name,
            sort_by=sort_by,
        )

    async def get_organisation_invitees(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        email: Optional[str] = None,
        sort_by: Optional[InvitationSortingField] = None,
    ) -> ProxyResponse:
        return await self._proxy.get_organisation_invitees(
            organisation_id=organisation_id,
            page=page,
            per_page=per_page,
            email=email,
            sort_by=sort_by,
        )

    async def get_organisation_approvals(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        full_name: Optional[str] = None,
        sort_by: Optional[UserSortingField] = None,
    ) -> ProxyResponse:
        return await self._proxy.get_organisation_approvals(
            organisation_id=organisation_id,
            page=page,
            per_page=per_page,
            full_name=full_name,
            sort_by=sort_by,
        )

    async def create_organisation(
        self,
        organisation_id: Optional[str],
        name: str,
        customization_url: Optional[str] = None,
    ) -> ProxyResponse:
        return await self._proxy.create_organisation(
            organisation_id=organisation_id,
            name=name,
            customization_url=customization_url,
        )

    async def delete_organisation(self, organisation_id: str) -> ProxyResponse:
        return IAMConsolidator.consolidate_deleting_organisation(await self._proxy.delete_organisation(organisation_id))

    async def update_organisation(
        self,
        organisation_id: str,
        name: Optional[str],
        customization_url: Optional[str],
    ) -> ProxyResponse:
        return await self._proxy.update_organisation(
            organisation_id=organisation_id,
            name=name,
            customization_url=customization_url,
        )

    async def get_user(self, user_id: str) -> ProxyResponse:
        return await self._proxy.get_user(user_id)
