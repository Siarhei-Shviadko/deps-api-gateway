from typing import Optional, Protocol

from ..proxy_response import ProxyResponse
from ..types import InvitationSortingField, UserSortingField

__all__ = ["IIAMProxy"]


class IIAMProxy(Protocol):
    async def activate_user_organisation(self, organisation_id: str) -> ProxyResponse:
        ...

    async def invite_user_to_organisation(self, organisation_id: str, emails: list[str]) -> ProxyResponse:
        ...

    async def join_organisation(self, organisation_id: str) -> ProxyResponse:
        ...

    async def approve_user_requests(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        ...

    async def delete_approvals(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        ...

    async def delete_users_from_organisation(self, organisation_id: str, user_ids: list[str]) -> ProxyResponse:
        ...

    async def delete_invitees_from_organisation(self, organisation_id: str, invitees: list[str]) -> ProxyResponse:
        ...

    async def create_user(
        self,
        email: str,
        username: Optional[str] = None,
        first_name: Optional[str] = "",
        last_name: Optional[str] = "",
        organisation: Optional[str] = None,
        create_api_key: bool = False,
    ) -> ProxyResponse:
        ...

    async def get_current_user(self) -> ProxyResponse:
        ...

    async def get_user_api_key(self) -> ProxyResponse:
        ...

    async def generate_user_api_key(self) -> ProxyResponse:
        ...

    async def revoke_user_api_key(self) -> ProxyResponse:
        ...

    async def get_user_organisations(self) -> ProxyResponse:
        ...

    async def get_organisation_detail(self, organisation_id: str) -> ProxyResponse:
        ...

    async def get_organisation_users(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        full_name: Optional[str] = None,
        sort_by: Optional[UserSortingField] = None,
    ) -> ProxyResponse:
        ...

    async def get_organisation_invitees(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        email: Optional[str] = None,
        sort_by: Optional[InvitationSortingField] = None,
    ) -> ProxyResponse:
        ...

    async def get_organisation_approvals(
        self,
        organisation_id: str,
        page: int = 1,
        per_page: int = 10,
        full_name: Optional[str] = None,
        sort_by: Optional[UserSortingField] = None,
    ) -> ProxyResponse:
        ...

    async def create_organisation(
        self,
        organisation_id: Optional[str],
        name: str,
        customization_url: Optional[str] = None,
    ) -> ProxyResponse:
        ...

    async def delete_organisation(self, organisation_id: str) -> ProxyResponse:
        ...

    async def update_organisation(
        self,
        organisation_id: str,
        name: Optional[str],
        customization_url: Optional[str],
    ) -> ProxyResponse:
        ...

    async def get_user(self, user_id: str) -> ProxyResponse:
        ...
