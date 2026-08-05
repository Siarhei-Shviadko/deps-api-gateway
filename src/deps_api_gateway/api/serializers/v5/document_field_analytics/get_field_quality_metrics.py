from datetime import datetime
from typing import Optional

from fastapi.params import Query

from ...base import ConfiguredBaseModel

__all__ = ["GetFieldQualityMetricsRequest", "GetFieldQualityMetricsResponse"]


class GetFieldQualityMetricsRequest(ConfiguredBaseModel):
    field_code: str = Query(...)
    document_type_id: str = Query(...)
    from_date: Optional[datetime] = Query(default=None)
    to_date: Optional[datetime] = Query(default=None)


class GetFieldQualityMetricsResponse(ConfiguredBaseModel):
    field_code: str
    document_type_id: str
    documents_with_misses: int
    documents_with_modifications: int
    total_modifications: int
    document_type_name: Optional[str] = None
    field_name: Optional[str] = None
