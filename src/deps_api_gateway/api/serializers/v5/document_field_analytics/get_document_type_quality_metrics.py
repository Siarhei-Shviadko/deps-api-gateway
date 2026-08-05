from datetime import datetime
from typing import Optional

from fastapi.params import Query

from ...base import ConfiguredBaseModel

__all__ = [
    "GetDocumentTypeQualityMetricsRequest",
    "DocumentTypeQualityInfo",
    "GetDocumentTypeQualityMetricsResponse",
]


class GetDocumentTypeQualityMetricsRequest(ConfiguredBaseModel):
    from_date: Optional[datetime] = Query(default=None)
    to_date: Optional[datetime] = Query(default=None)


class DocumentTypeQualityInfo(ConfiguredBaseModel):
    document_type_id: str
    total_fields_tracked: int
    total_fields_missed: int
    total_modifications: int
    documents_with_modifications: int
    document_type_name: Optional[str] = None


class GetDocumentTypeQualityMetricsResponse(ConfiguredBaseModel):
    items: list[DocumentTypeQualityInfo]  # noqa: WPS110
