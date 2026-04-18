from datetime import datetime
from typing import Optional

from fastapi.params import Query
from pydantic import Field

from ...base import ConfiguredBaseModel
from .paginated_result_metadata import PaginatedResultMetadata

__all__ = ["GetGroupsRequest", "GetGroupsResponse"]


class GroupsMetadata(PaginatedResultMetadata):
    pass


class Group(ConfiguredBaseModel):
    id: str
    name: str
    document_type_ids: list[str] = Field(..., alias="documentTypeIds")
    created_at: datetime = Field(..., alias="createdAt")


class GetGroupsRequest(ConfiguredBaseModel):
    name: Optional[str] = Query(default=None)
    document_type_id: Optional[str] = Query(default=None, alias="documentTypeId")
    date_start: Optional[str] = Query(default=None, alias="dateStart")
    date_end: Optional[str] = Query(default=None, alias="dateEnd")
    page: Optional[int] = Query(default=None, ge=0)
    per_page: Optional[int] = Query(default=None, alias="perPage", ge=0)
    sort_by: Optional[str] = Query(default="createdAt", alias="sortBy")
    sort_order: Optional[str] = Query(default="desc", alias="sortOrder")


class GetGroupsResponse(ConfiguredBaseModel):
    metadata: GroupsMetadata = Field(..., alias="meta")
    groups: list[Group] = Field(..., alias="result")
