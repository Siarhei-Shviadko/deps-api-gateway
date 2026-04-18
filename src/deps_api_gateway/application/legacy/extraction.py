from typing import Any, Optional

from deps_api_gateway.application import FieldType

from ..iproxies import IExtraction
from ..proxy_response import ProxyResponse

__all__ = ["ExtractionService"]


class ExtractionService:
    def __init__(self, extraction_proxy: IExtraction) -> None:
        self._extraction_proxy = extraction_proxy

    async def create_extraction_field(
        self,
        document_type_id: str,
        name: str,
        field_type: FieldType,
        required: bool,
        confidential: bool,
        read_only: bool,
        description: Optional[dict[str, Any]],
        order: int,
        extractor_id: Optional[str] = None,
        field_code: Optional[str] = None,
    ) -> ProxyResponse:
        return await self._extraction_proxy.create_field(
            document_type_id=document_type_id,
            name=name,
            field_type=field_type,
            required=required,
            confidential=confidential,
            read_only=read_only,
            description=description,
            order=order,
            extractor_id=extractor_id,
            field_code=field_code,
        )

    async def update_extraction_field(
        self,
        document_type_id: str,
        code: str,
        name: Optional[str],
        required: Optional[bool],
        confidential: Optional[bool],
        read_only: Optional[bool],
        description: Optional[dict[str, Any]],
        order: Optional[int],
        extractor_id: Optional[str] = None,
    ) -> ProxyResponse:
        return await self._extraction_proxy.update_field(
            document_type_id=document_type_id,
            field_code=code,
            name=name,
            description=description,
            required=required,
            confidential=confidential,
            read_only=read_only,
            order=order,
            extractor_id=extractor_id,
        )
