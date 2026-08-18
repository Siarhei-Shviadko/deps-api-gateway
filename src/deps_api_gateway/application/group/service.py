import asyncio
import logging
from typing import Awaitable, Optional, TypedDict

from deps_api_gateway.domain.exceptions import BaseApiGatewayException

from ..iproxies import IClassificationProxy
from ..proxy_response import ProxyResponse
from ..splitter import ISplittingProxy
from .consolidator import GroupsConsolidator
from .group_extras import GetGroupExtras, GetGroupsExtras
from .groups_proxy import IGroupsProxy

__all__ = ["GroupService", "GEN_AI_CLASSIFIER_NAME_MAX_LENGTH"]

GEN_AI_CLASSIFIER_NAME_MAX_LENGTH = 120


class _GroupsResponse(TypedDict, total=True):
    groups_response: ProxyResponse


class _GetGroupResponses(_GroupsResponse, total=False):
    classification_response: ProxyResponse
    splitter_response: Optional[ProxyResponse]


class GroupService:
    def __init__(
        self,
        groups_proxy: IGroupsProxy,
        classification_proxy: IClassificationProxy,
        splitter_proxy: ISplittingProxy,
    ) -> None:
        self._groups_proxy = groups_proxy
        self._classification_proxy = classification_proxy
        self._splitter_proxy = splitter_proxy

        self._logger = logging.getLogger(self.__class__.__name__)

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
        extras: Optional[list[GetGroupsExtras]] = None,
    ) -> ProxyResponse:
        if not extras or GetGroupsExtras.SPLITTERS not in extras:
            return await self._groups_proxy.get_groups(
                name=name,
                document_type_id=document_type_id,
                date_start=date_start,
                date_end=date_end,
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                sort_order=sort_order,
            )

        groups_response, splittings_response = await asyncio.gather(
            self._groups_proxy.get_groups(
                name=name,
                document_type_id=document_type_id,
                date_start=date_start,
                date_end=date_end,
                page=page,
                per_page=per_page,
                sort_by=sort_by,
                sort_order=sort_order,
            ),
            self._find_splitters_safely(),
        )

        return GroupsConsolidator.consolidate_groups(
            groups_response=groups_response,
            splittings_response=splittings_response,
        )

    async def get_group(self, group_id: str, extras: Optional[list[GetGroupExtras]]) -> ProxyResponse:
        result_dict: _GetGroupResponses = await self._gather_get_group_requests(
            group_id=group_id,
            extras=extras,
        )

        return GroupsConsolidator.consolidate_group(
            groups_response=result_dict["groups_response"],
            classification_response=result_dict.get("classification_response"),
            splitter_response=result_dict.get("splitter_response"),
        )

    async def create_group(
        self,
        name: str,
        document_type_ids: list[str],
    ) -> ProxyResponse:
        return await self._groups_proxy.create_group(
            name=name,
            document_type_ids=document_type_ids,
        )

    async def delete_groups(self, ids: list[str]) -> ProxyResponse:
        return await self._groups_proxy.delete_groups(
            ids=ids,
        )

    async def add_document_types(self, group_id: str, document_type_ids: list[str]) -> ProxyResponse:
        return await self._groups_proxy.add_document_types(
            group_id=group_id,
            document_type_ids=document_type_ids,
        )

    async def remove_document_types(self, group_id: str, document_type_ids: list[str]) -> ProxyResponse:
        return await self._groups_proxy.remove_document_types(
            group_id=group_id,
            document_type_ids=document_type_ids,
        )

    async def update_group_info(self, group_id: str, name: str) -> ProxyResponse:
        return await self._groups_proxy.update_group_info(
            group_id=group_id,
            name=name,
        )

    async def create_gen_ai_classifier(
        self,
        group_id: str,
        document_type_id: str,
        prompt: str,
        llm_type: str,
        name: str,
    ) -> ProxyResponse:
        return await self._classification_proxy.create_gen_ai_classifier(
            group_id=group_id,
            document_type_id=document_type_id,
            prompt=prompt,
            llm_type=llm_type,
            name=name,
        )

    async def update_gen_ai_classifier(
        self,
        gen_ai_classifier_id: str,
        prompt: Optional[str],
        llm_type: Optional[str],
        name: Optional[str],
    ) -> ProxyResponse:
        return await self._classification_proxy.update_gen_ai_classifier(
            gen_ai_classifier_id=gen_ai_classifier_id,
            prompt=prompt,
            llm_type=llm_type,
            name=name,
        )

    async def delete_gen_ai_classifiers(self, ids: list[str]) -> ProxyResponse:
        return await self._classification_proxy.delete_gen_ai_classifiers(ids=ids)

    async def get_classifiers_of_group(self, group_id: str) -> ProxyResponse:
        return await self._classification_proxy.get_gen_ai_classifiers_of_group(group_id)

    async def get_splitters(self, group_id: str) -> ProxyResponse:
        return await self._splitter_proxy.find_splitters(group_id)

    async def _find_splitters_safely(self, group_id: Optional[str] = None) -> Optional[ProxyResponse]:
        try:
            return await self._splitter_proxy.find_splitters(group_id)
        except BaseApiGatewayException:
            self._logger.warning(
                "Failed to fetch splitters for group_id=%s; falling back to no splitter data",
                group_id,
            )
            return None

    async def _gather_get_group_requests(
        self, group_id: str, extras: Optional[list[GetGroupExtras]]
    ) -> _GetGroupResponses:
        coroutines: dict[str, Awaitable[Optional[ProxyResponse]]] = {
            "groups_response": self._groups_proxy.get_group(group_id)
        }

        if extras:
            if GetGroupExtras.CLASSIFIERS in extras:
                coroutines["classification_response"] = self._classification_proxy.get_gen_ai_classifiers_of_group(
                    group_id
                )
            if GetGroupExtras.SPLITTERS in extras:
                coroutines["splitter_response"] = self._find_splitters_safely(group_id)

        return _GetGroupResponses(zip(coroutines.keys(), await asyncio.gather(*coroutines.values())))  # type: ignore
