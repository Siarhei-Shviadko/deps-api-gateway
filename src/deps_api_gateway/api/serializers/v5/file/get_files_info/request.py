from fastapi.params import Query
from pydantic import Field

from ....base import ConfiguredBaseModel

__all__ = ["GetFilesRequest"]


class GetFilesRequest(ConfiguredBaseModel):
    name: str | None = Query(default=None)
    labels: list[str] | None = Field(Query(None))
    date_start: str | None = Query(default=None, alias="dateStart")
    date_end: str | None = Query(default=None, alias="dateEnd")
    page: int | None = Query(default=None, ge=0)
    per_page: int | None = Query(default=None, alias="perPage", ge=0)
    sort_by: str = Query(default="createdAt", alias="sortBy")
    sort_order: str = Query(default="desc", alias="sortOrder")
    reference_available: bool | None = Query(default=None, alias="referenceAvailable")
    reference: str | None = Query(default=None)
