from typing import Optional

from fastapi import Query
from pydantic import conint

from deps_api_gateway.domain.dtos import (
    DocumentListFilter,
    SortingDirectionEnum,
    SortingFieldsEnum,
)

from ...base import ConfiguredBaseModel

__all__ = ["DocumentListFilterRequest"]


class DocumentListFilterRequest(ConfiguredBaseModel):
    title: Optional[str] = Query(None)
    datetime_range: Optional[str] = Query(None, alias="dateRange")
    types: Optional[str] = Query(None)
    states: Optional[str] = Query(None)
    engines: Optional[str] = Query(None)
    labels: Optional[str] = Query(None)
    reviewer: Optional[str] = Query(None)
    language: Optional[str] = Query(None)
    sort_field: SortingFieldsEnum = Query(SortingFieldsEnum.pk, alias="sortField")
    sorting_direction: SortingDirectionEnum = Query(SortingDirectionEnum.desc, alias="sortDirect")
    page: conint(ge=1) = Query(1)  # type: ignore[valid-type]
    per_page: conint(ge=1) = Query(10, alias="perPage")  # type: ignore[valid-type]
    search: Optional[str] = Query(None)
    filter_ids: Optional[str] = Query(None, alias="filterIds")
    groups: Optional[str] = Query(None)

    def to_model(self, *, raw_query: str) -> DocumentListFilter:
        return DocumentListFilter(
            title=self.title,
            datetime_range=self.datetime_range,
            types=self.types,
            states=self.states,
            engines=self.engines,
            labels=self.labels,
            reviewer=self.reviewer,
            language=self.language,
            sort_field=self.sort_field,
            sorting_direction=self.sorting_direction,
            page=self.page,
            per_page=self.per_page,
            search=self.search,
            raw_query=raw_query,
            filter_ids=self.filter_ids,
            groups=self.groups,
        )
