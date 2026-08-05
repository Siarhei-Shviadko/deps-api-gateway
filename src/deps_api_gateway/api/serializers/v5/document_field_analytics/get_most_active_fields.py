from datetime import datetime
from typing import Optional

from fastapi.params import Query

from ...base import ConfiguredBaseModel

__all__ = ["GetMostActiveFieldsRequest", "ActiveFieldInfo", "GetMostActiveFieldsResponse"]


class GetMostActiveFieldsRequest(ConfiguredBaseModel):
    limit: Optional[int] = Query(default=None)
    from_date: Optional[datetime] = Query(default=None)
    to_date: Optional[datetime] = Query(default=None)


class ActiveFieldInfo(ConfiguredBaseModel):
    field_code: str
    document_type_id: str
    modification_count: int
    documents_with_modifications: int
    document_type_name: Optional[str] = None
    field_name: Optional[str] = None


class GetMostActiveFieldsResponse(ConfiguredBaseModel):
    items: list[ActiveFieldInfo]  # noqa: WPS110
    total_count: int
