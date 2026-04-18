from typing import Any, Optional, Protocol

from ..proxy_response import ProxyResponse
from ..types import RawPoint
from .page_batch import PageBatch
from .parsing_feature import ParsingFeature
from .parsing_type import ParsingType

__all__ = ["IParsingProxy"]


class IParsingProxy(Protocol):
    async def find_document_layout(self, layout_id: str) -> dict[str, Any]:
        ...

    async def get_document_layout_info(self, layout_id: str) -> ProxyResponse:
        ...

    async def get_pages(
        self,
        document_layout_id: str,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
        batch_index: int = PageBatch.index,
        batch_size: int = PageBatch.size,
    ) -> dict[str, Any]:
        ...

    async def get_document_layout(
        self,
        document_layout_id: str,
        parsing_type: ParsingType,
        features: Optional[set[ParsingFeature]] = None,
        batch_index: Optional[int] = None,
        batch_size: Optional[int] = None,
    ) -> ProxyResponse:
        ...

    async def get_parsing_info(
        self,
        document_id: str,
    ) -> ProxyResponse:
        ...

    async def get_tabular_layout(
        self,
        tabular_layout_id: str,
        tables: Optional[list[str]],
        row_span: Optional[tuple[int, int]],
        col_span: Optional[tuple[int, int]],
    ) -> ProxyResponse:
        ...

    async def clone_document_layout(self, document_id: str, parsing_type: str) -> ProxyResponse:
        ...

    async def update_paragraph(
        self,
        document_layout_id: str,
        page_id: str,
        paragraph_id: str,
        update_paragraph_request: dict[str, Any],
    ) -> ProxyResponse:
        ...

    async def update_document_layout_image(
        self,
        document_id: str,
        page_id: str,
        image_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        filepath: Optional[str] = None,
        polygon: Optional[list[RawPoint]] = None,
    ) -> ProxyResponse:
        ...

    async def update_table(
        self,
        document_layout_id: str,
        page_id: str,
        table_id: str,
        update_table_request: dict[str, Any],
    ) -> ProxyResponse:
        ...

    async def update_key_value_pair(
        self,
        document_layout_id: str,
        page_id: str,
        key_value_pair_id: str,
        update_key_value_pair_request: dict[str, Any],
    ) -> ProxyResponse:
        ...
