from typing import Optional

from fastapi.params import Query

from ...base import ConfiguredBaseModel
from .field_value_snapshot import FieldValueSnapshot

__all__ = [
    "GetAllAnalyticsForFieldRequest",
    "DocumentFieldSummaryInfo",
    "GetAllAnalyticsForFieldResponse",
]


class GetAllAnalyticsForFieldRequest(ConfiguredBaseModel):
    field_code: str = Query(...)
    document_type_id: str = Query(...)
    page: Optional[int] = Query(default=None, ge=0)
    per_page: Optional[int] = Query(default=None, ge=0)


class DocumentFieldSummaryInfo(ConfiguredBaseModel):
    document_id: str
    modification_count: int
    has_miss: bool
    current_value: FieldValueSnapshot | None
    last_modified_by: Optional[str]
    last_modified_at: Optional[str]
    document_type_name: Optional[str] = None
    field_name: Optional[str] = None


class GetAllAnalyticsForFieldResponse(ConfiguredBaseModel):
    items: list[DocumentFieldSummaryInfo]  # noqa: WPS110
    total_count: int
    document_type_name: Optional[str] = None
    field_name: Optional[str] = None
