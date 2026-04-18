import json
from http import HTTPStatus
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IDocument
from deps_api_gateway.domain.exceptions import DocumentError, UploadDocumentError

from ..generic_rest_client import OldGenericRestClient

__all__ = ["OldDocumentProxy"]


class OldDocumentProxy(OldGenericRestClient, IDocument):
    async def upload_document(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise UploadDocumentError("Can't upload document")

        return response

    async def list_documents(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        response = await self.request(method, url, query, headers, data)
        if response["status_code"] != HTTPStatus.OK:
            raise DocumentError("Can't list documents")
        return response

    async def get_states(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict[str, Any]:
        response = await self.request(method, url, query, headers, data)
        if response["status_code"] != HTTPStatus.OK:
            raise DocumentError("Can't list states")
        return json.loads(response["content"])
