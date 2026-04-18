from http import HTTPStatus
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IUnifier
from deps_api_gateway.domain.exceptions import UnifiedDataError

from ..generic_rest_client import OldGenericRestClient

__all__ = ["OldUnifierProxy"]


class OldUnifierProxy(OldGenericRestClient, IUnifier):
    ALLOWED_STATUS_CODES = {HTTPStatus.OK, HTTPStatus.NOT_FOUND}

    async def get_unified_data(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] in self.ALLOWED_STATUS_CODES:
            return response

        raise UnifiedDataError("Can't get unified data!")
