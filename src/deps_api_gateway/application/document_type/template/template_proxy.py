from typing import Protocol

from ...proxy_response import ProxyResponse
from .data_type_code import TemplateDataTypeCode

__all__ = ["ITemplateProxy"]


class ITemplateProxy(Protocol):
    async def get_template_versions(self, document_type_id: str) -> ProxyResponse:
        ...

    async def get_template_version(self, document_type_id: str, version_id: str) -> ProxyResponse:
        ...

    async def update_template_version(self, document_type_id: str, version_id: str, name: str) -> ProxyResponse:
        ...

    async def delete_template_versions(self, document_type_id: str, version_ids: list[str]) -> ProxyResponse:
        ...

    async def add_markup(
        self,
        document_type_id: str,
        version_id: str,
        reference_page: str,
        markups: dict[str, list[list[float]]],
        markup_types: dict[str, TemplateDataTypeCode],
    ) -> ProxyResponse:
        ...
