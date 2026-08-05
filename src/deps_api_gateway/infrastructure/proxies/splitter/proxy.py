from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    ISplittingProxy,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.constants import SPLITTING_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import SplittingServiceUnavailableError

__all__ = ["SplittingProxy"]


class SplittingProxy(GenericRestClient, ISplittingProxy):
    exception = SplittingServiceUnavailableError
    v1_prefix = f"{SPLITTING_BASE_API_PREFIX}{V1_PREFIX}"

    async def find_splitters(self, group_id: str | None = None) -> ProxyResponse:
        params = {"groupId": group_id} if group_id is not None else {}
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v1_prefix}/splitters",
                    params=params,
                )
            )

    async def find_splitter_for(self, group_id: str, document_type_id: Optional[str]) -> ProxyResponse:
        params = {"groupId": group_id}
        if document_type_id is not None:
            params["documentTypeId"] = document_type_id

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v1_prefix}/splitters/resolve",
                    params=params,
                )
            )

    async def find_splitter(self, splitter_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.v1_prefix}/splitters/{splitter_id}"),
            )

    async def create_splitter(self, data: dict) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.v1_prefix}/splitters",
                    json=data,
                )
            )

    async def update_splitter(self, splitter_id: str, data: dict) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v1_prefix}/splitters/{splitter_id}",
                    json=data,
                )
            )

    async def remove_splitter(self, splitter_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=f"{self.v1_prefix}/splitters/{splitter_id}"),
            )

    async def get_proposal(self, proposal_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.GET, url=f"{self.v1_prefix}/splitting-proposals/{proposal_id}"),
            )

    async def update_proposal(self, proposal_id: str, data: dict) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v1_prefix}/splitting-proposals/{proposal_id}",
                    json=data,
                )
            )

    async def confirm_proposal(self, proposal_id: str) -> ProxyResponse:
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.v1_prefix}/splitting-proposals/{proposal_id}/confirm",
                )
            )
