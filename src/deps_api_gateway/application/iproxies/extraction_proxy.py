from typing import Any, Optional, Protocol

from deps_api_gateway.domain import ExtractionFieldData

from ..proxy_response import ProxyResponse
from ..types import ExtractorType, FieldType, SaveExtractedDataDTO, TableFieldUpdateData

__all__ = ["IExtraction"]


class IExtraction(Protocol):
    async def get_document_types(self) -> dict[str, Any]:
        ...

    async def get_document_type(self, document_type_id: str) -> dict[str, Any]:
        ...

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
        ...

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
        ...

    async def update_fields(
        self,
        document_type_id: str,
        fields: list[ExtractionFieldData],
    ) -> ProxyResponse:
        ...

    async def delete_fields(self, document_type_id: str, field_codes: list[str]) -> ProxyResponse:
        ...

    async def get_extraction_document_type(self, document_type_id: str) -> ProxyResponse:
        ...

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
        ...

    async def update_aliases(self, document_id: str, field_code: str, aliases: dict[str, str]) -> ProxyResponse:
        ...

    async def get_extracted_data(self, document_id: str, rows_per_chunk: Optional[int]) -> ProxyResponse:
        ...

    async def get_table_field_chunk(
        self,
        document_id: str,
        field_code: str,
        rows_per_chunk: int,
        rows_chunk: int,
        list_index: Optional[int],
    ) -> ProxyResponse:
        ...

    async def save_extracted_data(
        self,
        document_id: str,
        save_extracted_data_dto: SaveExtractedDataDTO,
    ) -> ProxyResponse:
        ...

    async def save_extracted_data_with_override(
        self,
        document_id: str,
        save_extracted_data_dto: SaveExtractedDataDTO,
    ) -> ProxyResponse:
        ...

    async def save_partial_extracted_data_field(
        self, document_id: str, field_code: str, field_data: TableFieldUpdateData
    ) -> ProxyResponse:
        ...

    async def get_document_type_v5(self, document_type_id: str) -> ProxyResponse:
        ...

    async def detach_extractor(self, document_type_id: str, extractor_id: str) -> ProxyResponse:
        ...
