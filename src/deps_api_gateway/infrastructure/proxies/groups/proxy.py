from typing import Any, Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IGroupsProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import GROUPS_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import GroupsError, GroupsServiceUnavailableError

__all__ = ["GroupsProxy"]


class GroupsProxy(GenericRestClient, IGroupsProxy):
    exception = GroupsError
    v1_prefix = f"{GROUPS_BASE_API_PREFIX}{V1_PREFIX}"

    async def get_groups(
        self,
        name: Optional[str],
        document_type_id: Optional[str],
        date_start: Optional[str],
        date_end: Optional[str],
        page: Optional[int],
        per_page: Optional[int],
        sort_by: str,
        sort_order: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups"

        data: dict[str, Any] = {
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        if name is not None:
            data["name"] = name

        if document_type_id is not None:
            data["documentTypeId"] = document_type_id

        if date_start is not None:
            data["dateStart"] = date_start

        if date_end is not None:
            data["dateEnd"] = date_end

        if page is not None:
            data["page"] = page

        if per_page is not None:
            data["perPage"] = per_page

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url, params=data))

        except Exception as error:
            raise GroupsServiceUnavailableError(error)

    async def get_group(self, group_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups/{group_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

        except Exception as error:
            raise GroupsServiceUnavailableError(error)

    async def create_group(
        self,
        name: str,
        document_type_ids: list[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups"

        data = {
            "name": name,
            "documentTypeIds": document_type_ids,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

        except Exception as error:
            raise GroupsServiceUnavailableError(error)

    async def delete_groups(self, ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups"

        params = {"id": ids}

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params=params)
            )

        except Exception as error:
            raise GroupsServiceUnavailableError(error)

    async def add_document_types(self, group_id: str, document_type_ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups/{group_id}/document-types"

        data = {"documentTypeIds": document_type_ids}

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

        except Exception as error:
            raise GroupsServiceUnavailableError(error)

    async def remove_document_types(self, group_id: str, document_type_ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups/{group_id}/document-types"

        params = {"id": document_type_ids}

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params=params)
            )

        except Exception as error:
            raise GroupsServiceUnavailableError(error)

    async def update_group_info(self, group_id: str, name: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/groups/{group_id}"

        data = {
            "name": name,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

        except Exception as error:
            raise GroupsServiceUnavailableError(error)
