import asyncio
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.api.utilities import ReferenceLayoutResponse
from deps_api_gateway.constants import UNIFIER_BASE_API_PREFIX, V1_PREFIX

from ...parsing import IParsingProxy
from ..unifier_proxy import IUnifier
from .prototype_proxy import ILegacyPrototypeProxy

__all__ = ["PrototypeService"]


class PrototypeService:
    def __init__(
        self, prototype_proxy: ILegacyPrototypeProxy, unifier_proxy: IUnifier, parsing_proxy: IParsingProxy
    ) -> None:
        self._prototype_proxy = prototype_proxy
        self._unifier_proxy = unifier_proxy
        self._parsing_proxy = parsing_proxy

    async def find_layouts(self, prototype_id: str) -> dict[str, Any]:
        return await self._prototype_proxy.find_layouts(prototype_id)

    async def find_layout(self, prototype_id: str, reference_layout_id: str, deps_token: str) -> dict[str, Any]:
        prototype_task = self._prototype_proxy.find_layout(prototype_id=prototype_id, layout_id=reference_layout_id)
        unifier_task = self._unifier_proxy.get_unified_data(
            method=Methods.GET,
            url=f"{UNIFIER_BASE_API_PREFIX}{V1_PREFIX}/unified_data/{reference_layout_id}",
            query="",
            headers={"deps-token": deps_token},
            data=b"",
        )
        parsing_task = self._parsing_proxy.find_document_layout(layout_id=reference_layout_id)

        prototype_task_result, unifier_task_result, parsing_task_result = await asyncio.gather(
            asyncio.create_task(prototype_task),
            asyncio.create_task(unifier_task),
            asyncio.create_task(parsing_task),
            return_exceptions=True,
        )
        return ReferenceLayoutResponse(prototype_task_result, unifier_task_result, parsing_task_result).make_response()

    async def delete_layout(self, prototype_id: str, layout_id: str) -> None:
        await self._prototype_proxy.delete_layout(prototype_id=prototype_id, layout_id=layout_id)

    async def delete_layouts(self, prototype_id: str, layout_ids: list[str]) -> None:
        await self._prototype_proxy.delete_layouts(prototype_id=prototype_id, layout_ids=layout_ids)
