from dataclasses import dataclass
from enum import Enum
from typing import Optional

__all__ = ["DocumentListFilter", "SortingFieldsEnum", "SortingDirectionEnum"]


class SortingFieldsEnum(Enum):
    pk = "pk"
    title = "title"
    state = "state"
    document_type = "documentType"
    date = "date"
    source = "source"
    reviewer = "reviewer"
    engine = "engine"
    group = "group"


class SortingDirectionEnum(Enum):
    asc = "asc"
    desc = "desc"


@dataclass(frozen=True)
class DocumentListFilter:
    title: Optional[str]
    datetime_range: Optional[str]
    types: Optional[str]
    states: Optional[str]
    engines: Optional[str]
    labels: Optional[str]
    reviewer: Optional[str]
    language: Optional[str]
    sort_field: SortingFieldsEnum
    sorting_direction: SortingDirectionEnum
    page: int
    per_page: int
    search: Optional[str]
    raw_query: str
    filter_ids: Optional[str]
    groups: Optional[str]
