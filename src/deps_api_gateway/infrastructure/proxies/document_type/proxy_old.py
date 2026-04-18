import json
from http import HTTPStatus
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IDocumentTypeOld
from deps_api_gateway.domain.exceptions import DocumentTypeError, NotFoundError

from ..generic_rest_client import OldGenericRestClient

__all__ = ["DocumentTypeProxyOld"]


class DocumentTypeProxyOld(OldGenericRestClient, IDocumentTypeOld):
    async def get_document_types(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise DocumentTypeError("Can't get document types!")

        return json.loads(response["content"])

    async def get_document_type(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise NotFoundError("Document type was not found.")

        return json.loads(response["content"])
