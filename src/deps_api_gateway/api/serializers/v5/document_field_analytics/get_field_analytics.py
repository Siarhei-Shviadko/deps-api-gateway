from typing import Optional

from fastapi.params import Query

from ...base import ConfiguredBaseModel
from .field_value_snapshot import FieldValueSnapshot

__all__ = [
    "GetFieldAnalyticsRequest",
    "FieldModificationInfo",
    "FieldMissInfo",
    "GetFieldAnalyticsResponse",
]


class GetFieldAnalyticsRequest(ConfiguredBaseModel):
    document_id: str = Query(...)
    field_code: str = Query(...)


class FieldModificationInfo(ConfiguredBaseModel):
    old_value: FieldValueSnapshot
    new_value: FieldValueSnapshot
    modified_by: str
    modified_at: str


class FieldMissInfo(ConfiguredBaseModel):
    missed_at: str


class GetFieldAnalyticsResponse(ConfiguredBaseModel):
    id: str
    document_id: str
    field_code: str
    document_type_id: str
    modifications: list[FieldModificationInfo]
    miss: Optional[FieldMissInfo]
    modification_count: int
    has_miss: bool
    current_value: FieldValueSnapshot | None
    document_type_name: Optional[str] = None
    field_name: Optional[str] = None
