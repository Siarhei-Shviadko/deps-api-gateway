import json
from http import HTTPStatus
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IOCR
from deps_api_gateway.domain.exceptions import OCRError
from deps_api_gateway.infrastructure.proxies.generic_rest_client import (
    OldGenericRestClient,
)

__all__ = ["OldOCRProxy"]


class OldOCRProxy(OldGenericRestClient, IOCR):
    async def get_languages(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        response = await self.request(method=method, url=url, query=query, headers=headers, data=data)
        if response["status_code"] != HTTPStatus.OK:
            raise OCRError("Can't get languages")
        return json.loads(response["content"])

    async def get_engines(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> list[dict[str, str]]:
        response = await self.request(method=method, url=url, query=query, headers=headers, data=data)
        if response["status_code"] != HTTPStatus.OK:
            raise OCRError("Can't get engines")
        return json.loads(response["content"])
