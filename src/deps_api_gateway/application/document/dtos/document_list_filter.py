from datetime import datetime
from typing import Optional, TypedDict

from deps_api_gateway.domain import SortingDirectionEnum, SortingFieldsEnum

from ..state import DocumentState

__all__ = ["DocumentListFilterData"]


class DocumentListFilterData(TypedDict, total=False):
    states: Optional[list[DocumentState]]
    types: Optional[list[str]]
    title: Optional[str]
    exceptTypes: Optional[list[str]]
    reviewer: Optional[str]
    engines: Optional[list[str]]
    sortField: SortingFieldsEnum
    sortDirect: SortingDirectionEnum
    page: int
    perPage: int
    labels: Optional[list[str]]
    dateRange: Optional[list[datetime]]
    hasReviewer: Optional[bool]
    search: Optional[str]
    filterIds: Optional[list[str]]
    groups: Optional[list[str]]
    parentId: Optional[str]
