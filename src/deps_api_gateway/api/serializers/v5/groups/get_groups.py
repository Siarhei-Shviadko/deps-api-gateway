from datetime import datetime
from typing import Optional

from fastapi.params import Query
from pydantic import Field

from deps_api_gateway.application import GetGroupsExtras

from ...base import ConfiguredBaseModel
from .paginated_result_metadata import PaginatedResultMetadata

__all__ = ["GetGroupsRequest", "GetGroupsResponse", "SplitterInfo"]


class GroupsMetadata(PaginatedResultMetadata):
    pass


class SplitterInfo(ConfiguredBaseModel):
    splitter_id: str
    splitter_name: str
    splitter_description: str
    group_id: str
    document_type_id: Optional[str]


class Group(ConfiguredBaseModel):
    id: str
    name: str
    document_type_ids: list[str] = Field(..., alias="documentTypeIds")
    created_at: datetime = Field(..., alias="createdAt")
    splitter: Optional[SplitterInfo] = Field(None)


class GetGroupsRequest(ConfiguredBaseModel):
    name: Optional[str] = Query(default=None)
    document_type_id: Optional[str] = Query(default=None, alias="documentTypeId")
    date_start: Optional[str] = Query(default=None, alias="dateStart")
    date_end: Optional[str] = Query(default=None, alias="dateEnd")
    page: Optional[int] = Query(default=None, ge=0)
    per_page: Optional[int] = Query(default=None, alias="perPage", ge=0)
    sort_by: Optional[str] = Query(default="createdAt", alias="sortBy")
    sort_order: Optional[str] = Query(default="desc", alias="sortOrder")
    extras: Optional[list[GetGroupsExtras]] = Field(Query(default=None))


class GetGroupsResponse(ConfiguredBaseModel):
    metadata: GroupsMetadata = Field(..., alias="meta")
    groups: list[Group] = Field(..., alias="result")
