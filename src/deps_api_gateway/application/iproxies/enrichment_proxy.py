from typing import Protocol

from ...domain import ExtraFieldData
from ..proxy_response import ProxyResponse
from ..types import SaveExtraDataElement

__all__ = ["IEnrichmentProxy"]


class IEnrichmentProxy(Protocol):
    async def get_extra_fields(self, document_type_id: str) -> ProxyResponse:
        ...

    async def get_document_supplement(self, document_id: str) -> ProxyResponse:
        ...

    async def save_document_supplement(
        self,
        document_id: str,
        document_type_id: str,
        extra_data_list: list[SaveExtraDataElement],
    ) -> ProxyResponse:
        ...

    async def save_extra_fields(self, document_type_id: str, name: str, order: int) -> ProxyResponse:
        ...

    async def update_extra_fields(self, document_type_id: str, fields: list[ExtraFieldData]) -> ProxyResponse:
        ...

    async def delete_extra_fields(self, document_type_id: str, extra_field_codes: list[str]) -> ProxyResponse:
        ...
