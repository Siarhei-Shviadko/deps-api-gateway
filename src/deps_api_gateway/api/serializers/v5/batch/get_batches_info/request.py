from typing import Optional

from fastapi.params import Query

from ....base import ConfiguredBaseModel

__all__ = ["GetBatchesRequest"]


class GetBatchesRequest(ConfiguredBaseModel):
    name: Optional[str] = Query(default=None)
    page: Optional[int] = Query(default=None, ge=0)
    group: Optional[str] = Query(default=None, alias="group")
    date_start: Optional[str] = Query(default=None, alias="dateStart")
    date_end: Optional[str] = Query(default=None, alias="dateEnd")
    per_page: Optional[int] = Query(default=None, alias="perPage", ge=0)
    sort_by: str = Query(default="createdAt", alias="sortBy")
    sort_order: str = Query(default="desc", alias="sortOrder")
