from typing import Any, Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    ExtractorType,
    FieldType,
    IExtraction,
    ProxyResponse,
    ProxyResponseFactory,
    SaveExtractedDataDTO,
    TableFieldUpdateData,
)
from deps_api_gateway.constants import EXTRACTION_BASE_API_PREFIX, V1_PREFIX, V2_PREFIX
from deps_api_gateway.domain import ExtractionFieldData

from ..generic_rest_client import GenericRestClient
from .exceptions import ExtractionServiceUnavailableError

__all__ = ["ExtractionProxy"]


class ExtractionProxy(GenericRestClient, IExtraction):
    exception = ExtractionServiceUnavailableError
    v1_prefix = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}"
    v2_prefix = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}"

    async def get_document_types(self) -> dict[str, Any]:
        try:
            return await self.request(method=Methods.GET, url=f"{self.v1_prefix}/document-types")
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def get_document_type(self, document_type_id: str) -> dict[str, Any]:
        try:
            return await self.request(method=Methods.GET, url=f"{self.v1_prefix}/document-types/{document_type_id}")
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def get_extraction_document_type(self, document_type_id: str) -> ProxyResponse:
        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v1_prefix}/document-types/{document_type_id}",
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def create_field(
        self,
        document_type_id: str,
        name: str,
        field_type: FieldType,
        description: Optional[dict[str, Any]],
        required: bool,
        confidential: bool,
        read_only: bool,
        order: int,
        extractor_id: Optional[str],
        field_code: Optional[str],
    ) -> ProxyResponse:
        field_data = {
            "name": name,
            "type": field_type.value,
            "required": required,
            "confidential": confidential,
            "readOnly": read_only,
            "order": order,
            "extractorId": extractor_id,
        }
        if description is not None:
            field_data["description"] = description
        if field_code is not None:
            field_data["code"] = field_code

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.v2_prefix}/document-types/{document_type_id}/extraction-fields",
                    json=field_data,
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def update_field(
        self,
        document_type_id: str,
        field_code: str,
        name: Optional[str],
        description: Optional[dict[str, Any]],
        required: Optional[bool],
        confidential: Optional[bool],
        read_only: Optional[bool],
        order: Optional[int],
        extractor_id: Optional[str],
    ) -> ProxyResponse:
        field_data = {
            "description": description,
            "name": name,
            "required": required,
            "confidential": confidential,
            "readOnly": read_only,
            "order": order,
        }

        query_params = {"extractorId": extractor_id} if extractor_id is not None else {}

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v2_prefix}/document-types/{document_type_id}/extraction-fields/{field_code}",
                    json=field_data,
                    params=query_params,
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def update_fields(
        self,
        document_type_id: str,
        fields: list[ExtractionFieldData],
    ) -> ProxyResponse:
        fields_data = {
            "fields": [
                {
                    "code": field.code,
                    "name": field.name,
                    "description": field.description,
                    "required": field.required,
                    "read_only": field.read_only,
                    "confidential": field.confidential,
                    "order": field.order,
                }
                for field in fields
            ]
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v2_prefix}/document-types/{document_type_id}/extraction-fields",
                    json=fields_data,
                )
            )

    async def delete_fields(self, document_type_id: str, field_codes: list[str]) -> ProxyResponse:
        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.DELETE,
                    url=f"{self.v2_prefix}/document-types/{document_type_id}/extraction-fields",
                    params={"fieldCodes": field_codes},
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def attach_extractor(
        self,
        name: str,
        extractor_type: ExtractorType,
        fields: Optional[list[dict[str, Any]]] = None,
        description: Optional[str] = None,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        image_transformations: Optional[list[str]] = None,
    ) -> ProxyResponse:
        extractor_data = {
            "name": name,
            "extractorType": extractor_type.value,
            "engine": engine,
            "language": language,
            "imageTransformations": image_transformations,
            "fields": fields,
            "description": description,
        }
        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.POST,
                    url=f"{self.v2_prefix}/document-types/attach-extractor",
                    json=extractor_data,
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def update_aliases(self, document_id: str, field_code: str, aliases: dict[str, str]) -> ProxyResponse:
        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.PATCH,
                    url=f"{self.v2_prefix}/extracted-data/{document_id}/fields/{field_code}/aliases",
                    json={"updatedAliases": aliases},
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def get_extracted_data(self, document_id: str, rows_per_chunk: Optional[int]) -> ProxyResponse:
        data = {"rowsPerChunk": rows_per_chunk} if rows_per_chunk is not None else None

        try:
            return ProxyResponseFactory.make_response_from(
                await self.request(
                    method=Methods.GET,
                    url=f"{self.v2_prefix}/extracted-data/{document_id}",
                    params=data,
                )
            )
        except Exception as error:
            raise ExtractionServiceUnavailableError(error)

    async def get_table_field_chunk(
        self,
        document_id: str,
        field_code: str,
        rows_per_chunk: int,
        rows_chunk: int,
        list_index: Optional[int],
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/extracted-data/{document_id}/fields/{field_code}/chunk"

        data = {
            "rowsPerChunk": rows_per_chunk,
            "rowsChunk": rows_chunk,
        }
        if list_index is not None:
            data["listIndex"] = list_index

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url, params=data))

    async def save_extracted_data(
        self,
        document_id: str,
        save_extracted_data_dto: SaveExtractedDataDTO,
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/extracted-data/{document_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PUT, url=url, json=save_extracted_data_dto)
            )

    async def save_extracted_data_with_override(
        self,
        document_id: str,
        save_extracted_data_dto: SaveExtractedDataDTO,
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/extracted-data/{document_id}/override"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(
                await self.request(method=Methods.PUT, url=url, json=save_extracted_data_dto)
            )

    async def save_partial_extracted_data_field(
        self,
        document_id: str,
        field_code: str,
        field_data: TableFieldUpdateData,
    ) -> ProxyResponse:
        url = f"{self.v2_prefix}/extracted-data/{document_id}/fields/{field_code}"
        data: dict = field_data

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

    async def get_document_type_v5(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def detach_extractor(self, document_type_id: str, extractor_id: str) -> ProxyResponse:
        url = f"{self.v2_prefix}/document-types/{document_type_id}/extractors/{extractor_id}"
        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))
