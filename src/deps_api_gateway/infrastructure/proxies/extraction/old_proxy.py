from http import HTTPStatus
from typing import Any

from async_rest_client import Methods

from deps_api_gateway.application.legacy import IExtractionOld
from deps_api_gateway.domain.exceptions import ExtractedDataError

from ..generic_rest_client import OldGenericRestClient

__all__ = ["OldExtractionProxy"]


class OldExtractionProxy(OldGenericRestClient, IExtractionOld):
    ALLOWED_STATUS_CODES = {HTTPStatus.OK, HTTPStatus.NOT_FOUND}

    async def get_extracted_data(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] in self.ALLOWED_STATUS_CODES:
            return response

        raise ExtractedDataError("Can't get extracted data!")

    async def get_field_chunk(
        self,
        method: Methods,
        url: str,
        query: str,
        headers: dict[str, Any],
        data: bytes,
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] in self.ALLOWED_STATUS_CODES:
            return response

        raise ExtractedDataError("Can't get extracted data field chunk!")

    async def delete_extracted_fields(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise ExtractedDataError("Can't delete extracted field!")

        return response

    async def put_extracted_data_field(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise ExtractedDataError("Can't update extracted data field")

        return response

    async def update_extracted_data(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise ExtractedDataError("Can't update extracted data!")

        return response

    async def update_extracted_data_cells(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise ExtractedDataError("Can't update extracted data cells!")

        return response
