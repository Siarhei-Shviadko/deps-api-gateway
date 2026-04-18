from typing import Optional, Protocol

from starlette.datastructures import UploadFile

from ...proxy_response import ProxyResponse
from .data_type_code import PrototypeDataTypeCode
from .header import Header, HeaderType
from .mapping_type import MappingType

__all__ = ["IPrototypeProxy"]


class IPrototypeProxy(Protocol):
    async def create_mapping(
        self,
        document_type_id: str,
        code: str,
        data_type: PrototypeDataTypeCode,
        keys: list[str],
        mapping_type: MappingType,
    ) -> ProxyResponse:
        ...

    async def create_tabular_mapping(
        self,
        code: str,
        document_type_id: str,
        header_type: HeaderType,
        headers: list[Header],
        occurrence_index: int,
    ) -> ProxyResponse:
        ...

    async def update_mapping(
        self,
        document_type_id: str,
        code: str,
        keys: list[str],
    ) -> ProxyResponse:
        ...

    async def update_tabular_mapping(
        self,
        document_type_id: str,
        code: str,
        header_type: Optional[HeaderType],
        headers: Optional[list[Header]],
        occurrence_index: Optional[int],
    ) -> ProxyResponse:
        ...

    async def get_prototype(
        self,
        document_type_id: str,
    ) -> ProxyResponse:
        ...

    async def create_prototype(
        self,
        name: str,
        engine: str,
        language: str,
        description: Optional[str],
    ) -> ProxyResponse:
        ...

    async def update_prototype(
        self,
        document_type_id: str,
        engine: Optional[str],
        language: Optional[str],
        description: Optional[str],
    ) -> ProxyResponse:
        ...

    async def get_reference_layouts(self, document_type_id: str) -> ProxyResponse:
        ...

    async def get_reference_layout(self, document_type_id: str, layout_id: str) -> ProxyResponse:
        ...

    async def create_reference_layout(self, document_type_id: str, file: UploadFile) -> ProxyResponse:
        ...

    async def delete_reference_layouts(self, document_type_id: str, layout_ids: list[str]) -> ProxyResponse:
        ...

    async def restart_reference_layout(self, document_type_id, layout_id: str) -> ProxyResponse:
        ...
