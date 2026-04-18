from typing import Optional

from ..iproxies import IExtraction
from ..proxy_response import ProxyResponse
from ..types import SaveExtractedDataDTO, TableFieldUpdateData

__all__ = ["ExtractionService"]


class ExtractionService:
    def __init__(
        self,
        extraction_proxy: IExtraction,
    ) -> None:
        self._extraction_proxy = extraction_proxy

    async def update_aliases(self, document_id: str, field_code: str, aliases: dict[str, str]) -> ProxyResponse:
        return await self._extraction_proxy.update_aliases(
            document_id=document_id, field_code=field_code, aliases=aliases
        )

    async def save_extracted_data(
        self, document_id: str, save_extracted_data_dto: SaveExtractedDataDTO
    ) -> ProxyResponse:
        return await self._extraction_proxy.save_extracted_data(
            document_id=document_id,
            save_extracted_data_dto=save_extracted_data_dto,
        )

    async def save_extracted_data_with_override(
        self, document_id: str, save_extracted_data_dto: SaveExtractedDataDTO
    ) -> ProxyResponse:
        return await self._extraction_proxy.save_extracted_data_with_override(
            document_id=document_id,
            save_extracted_data_dto=save_extracted_data_dto,
        )

    async def save_partial_extracted_data_field(
        self,
        document_id: str,
        field_code: str,
        field_data: TableFieldUpdateData,
    ) -> ProxyResponse:
        return await self._extraction_proxy.save_partial_extracted_data_field(
            document_id=document_id,
            field_code=field_code,
            field_data=field_data,
        )

    async def get_table_field_chunk(
        self,
        document_id: str,
        field_code: str,
        rows_per_chunk: int,
        rows_chunk: int,
        list_index: Optional[int],
    ) -> ProxyResponse:
        return await self._extraction_proxy.get_table_field_chunk(
            document_id=document_id,
            field_code=field_code,
            rows_per_chunk=rows_per_chunk,
            rows_chunk=rows_chunk,
            list_index=list_index,
        )
