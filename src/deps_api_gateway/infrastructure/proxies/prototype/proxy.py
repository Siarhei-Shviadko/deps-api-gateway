import json
from typing import Any, Optional

from aiohttp import FormData
from async_rest_client import Methods
from starlette.datastructures import UploadFile

from deps_api_gateway.application import (
    Header,
    HeaderType,
    IPrototypeProxy,
    MappingType,
    PrototypeDataTypeCode,
    ProxyResponse,
    ProxyResponseFactory,
)
from deps_api_gateway.application.legacy import ILegacyPrototypeProxy
from deps_api_gateway.constants import PROTOTYPE_BASE_API_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import PrototypeError, PrototypeServiceUnavailableError

__all__ = ["PrototypeProxy", "IBackwardCompatiblePrototypeProxy"]


class IBackwardCompatiblePrototypeProxy(IPrototypeProxy, ILegacyPrototypeProxy):
    pass


class PrototypeProxy(GenericRestClient, IBackwardCompatiblePrototypeProxy):
    exception = PrototypeError
    v1_prefix = f"{PROTOTYPE_BASE_API_PREFIX}{V1_PREFIX}/prototypes"

    async def find_layouts(self, prototype_id: str) -> dict[str, Any]:
        url = f"{self.v1_prefix}/{prototype_id}/layouts"
        data = {"prototypeId": prototype_id}

        response = await self.request(method=Methods.GET, url=url, json=data)

        self._check_response(response=response, url=url)

        return json.loads(response["content"])

    async def find_layout(self, prototype_id: str, layout_id: str) -> dict[str, Any]:
        url = f"{self.v1_prefix}/{prototype_id}/layouts/{layout_id}"

        response = await self.request(method=Methods.GET, url=url)
        self._check_response(response=response, url=url)

        return json.loads(response["content"])

    async def delete_layout(self, prototype_id: str, layout_id: str) -> None:
        url = f"{self.v1_prefix}/{prototype_id}/layouts/{layout_id}"

        response = await self.request(method=Methods.DELETE, url=url)

        self._check_response(response=response, url=url)

    async def delete_layouts(self, prototype_id: str, layout_ids: list[str]) -> None:
        url = f"{self.v1_prefix}/{prototype_id}/layouts"
        params = {"layoutIds": layout_ids}

        response = await self.request(method=Methods.DELETE, url=url, params=params)

        self._check_response(response=response, url=url)

    async def create_mapping(
        self,
        document_type_id: str,
        code: str,
        data_type: PrototypeDataTypeCode,
        keys: list[str],
        mapping_type: MappingType,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/mappings"
        data = {
            "code": code,
            "typeCode": data_type.value,
            "keys": keys,
            "mappingType": mapping_type.value,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise PrototypeServiceUnavailableError(error)

    async def create_tabular_mapping(
        self,
        code: str,
        document_type_id: str,
        header_type: HeaderType,
        headers: list[Header],
        occurrence_index: int,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/tabular-mappings"
        data = {
            "code": code,
            "header_type": header_type,
            "headers": headers,
            "occurrence_index": occurrence_index,
        }

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_mapping(
        self,
        document_type_id: str,
        code: str,
        keys: list[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/mappings/{code}"
        data = {
            "keys": keys,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PUT, url=url, json=data))
        except Exception as error:
            raise PrototypeServiceUnavailableError(error)

    async def update_tabular_mapping(
        self,
        document_type_id: str,
        code: str,
        header_type: Optional[HeaderType],
        headers: Optional[list[Header]],
        occurrence_index: Optional[int],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/tabular-mappings/{code}"

        data = {}
        if header_type is not None:
            data["headerType"] = header_type
        if headers is not None:
            data["headers"] = headers
        if occurrence_index is not None:
            data["occurrenceIndex"] = occurrence_index

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

    async def get_prototype(
        self,
        document_type_id: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise PrototypeServiceUnavailableError(error)

    async def create_prototype(
        self,
        name: str,
        engine: str,
        language: str,
        description: Optional[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}"

        data = {
            "name": name,
            "engine": engine,
            "language": language,
        }
        if description is not None:
            data["description"] = description

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))

    async def update_prototype(
        self,
        document_type_id: str,
        engine: Optional[str],
        language: Optional[str],
        description: Optional[str],
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}"
        data = {}
        if engine is not None:
            data["engine"] = engine
        if language is not None:
            data["language"] = language
        if description is not None:
            data["description"] = description

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

    async def get_reference_layouts(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/layouts"

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def get_reference_layout(self, document_type_id: str, layout_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/layouts/{layout_id}"

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def create_reference_layout(self, document_type_id: str, file: UploadFile) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/layouts"

        form_data = FormData()
        form_data.add_field(
            name="file",
            value=await file.read(),
            filename=file.filename,
            content_type=file.content_type,
        )

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.POST, url=url, data=form_data())
            )

    async def delete_reference_layouts(self, document_type_id: str, layout_ids: list[str]) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/layouts"

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.DELETE, url=url, params={"layoutIds": layout_ids})
            )

    async def restart_reference_layout(self, document_type_id, layout_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/{document_type_id}/layouts/{layout_id}/restart"

        async with self._handling_exception(PrototypeServiceUnavailableError):
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url))
