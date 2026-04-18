from typing import Optional, Protocol

from ..proxy_response import ProxyResponse
from ..types import CellsReference, ElementType

__all__ = ["IUnifierProxy"]


class IUnifierProxy(Protocol):
    async def get_unified_data(
        self,
        document_id: str,
        pos_text_blob_name: Optional[str] = None,
        unified_data_types: Optional[set[ElementType]] = None,
    ) -> ProxyResponse:
        ...

    async def get_unified_cells_data(
        self,
        document_id: str,
        table_id: str,
        reference: CellsReference,
    ) -> ProxyResponse:
        ...
