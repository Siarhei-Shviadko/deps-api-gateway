from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .table_field_chunk import TableFieldChunk

__all__ = ["TableChunkResponse", "TableFieldChunkMeta"]


class TableFieldChunkMeta(ConfiguredBaseModel):
    rows_chunk: int = Field(..., alias="rowsChunk")
    chunks_total: int = Field(..., alias="chunksTotal")
    rows_total: int = Field(..., alias="rowsTotal")
    list_index: Optional[int] = Field(None, alias="listIndex")


class TableChunkResponse(ConfiguredBaseModel):
    meta: TableFieldChunkMeta
    data: TableFieldChunk
