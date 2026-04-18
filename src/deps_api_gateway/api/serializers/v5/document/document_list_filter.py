from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import Field, conint

from deps_api_gateway.application.document import DocumentListFilterData, DocumentState
from deps_api_gateway.domain import SortingDirectionEnum, SortingFieldsEnum

from ...base import ConfiguredBaseModel

__all__ = ["DocumentListFilter"]


class DocumentListFilter(ConfiguredBaseModel):
    states: Optional[list[DocumentState]] = Field(Query(None))
    types: Optional[list[str]] = Field(Query(None))
    title: Optional[str] = Query(None)
    except_types: Optional[list[str]] = Field(Query(default=None), alias="exceptTypes")
    reviewer: Optional[str] = Query(None)
    engines: Optional[list[str]] = Field(Query(None))
    sorting_field: Optional[SortingFieldsEnum] = Field(Query(default=None), alias="sortField")
    sorting_direction: Optional[SortingDirectionEnum] = Field(Query(default=None), alias="sortDirect")
    page: Optional[conint(ge=1)] = Query(None)  # type: ignore[valid-type]
    per_page: Optional[conint(ge=1)] = Query(default=None, alias="perPage")  # type: ignore[valid-type]
    labels: Optional[list[str]] = Field(Query(None))
    datetime_range: Optional[list[datetime]] = Field(  # type: ignore
        Query(None, description="Must have exactly 2 values: start date and end date"),
        alias="dateRange",
        min_length=2,
        max_length=2,
    )
    has_reviewer: Optional[bool] = Query(default=None, alias="hasReviewer")
    search: Optional[str] = Query(None)
    filter_ids: Optional[list[int]] = Field(Query(default=None), alias="filterIds", min_length=1)
    groups: Optional[list[str]] = Field(Query(default=None))
    parent_id: Optional[str] = Field(Query(default=None), alias="parentId")

    def to_dto(self) -> DocumentListFilterData:
        return DocumentListFilterData(**self.model_dump(by_alias=True, exclude_none=True))
