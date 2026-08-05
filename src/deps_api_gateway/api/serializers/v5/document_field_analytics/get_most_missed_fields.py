from datetime import datetime
from typing import Optional

from fastapi.params import Query

from ...base import ConfiguredBaseModel

__all__ = ["GetMostMissedFieldsRequest", "MissedFieldInfo", "GetMostMissedFieldsResponse"]


class GetMostMissedFieldsRequest(ConfiguredBaseModel):
    limit: Optional[int] = Query(default=None)
    from_date: Optional[datetime] = Query(default=None)
    to_date: Optional[datetime] = Query(default=None)


class MissedFieldInfo(ConfiguredBaseModel):
    field_code: str
    document_type_id: str
    miss_count: int
    document_type_name: Optional[str] = None
    field_name: Optional[str] = None


class GetMostMissedFieldsResponse(ConfiguredBaseModel):
    items: list[MissedFieldInfo]  # noqa: WPS110
    total_count: int
