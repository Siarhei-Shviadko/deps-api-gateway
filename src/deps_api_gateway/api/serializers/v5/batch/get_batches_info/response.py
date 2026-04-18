from pydantic import Field

from ....base import ConfiguredBaseModel
from .batch import SerializedListBatchInfo
from .paginated_result_metadata import PaginatedResultMetadata

__all__ = ["GetBatchesResponse"]


class GetBatchesResponse(ConfiguredBaseModel):
    metadata: PaginatedResultMetadata = Field(..., alias="meta")
    batches: list[SerializedListBatchInfo] = Field(..., alias="result")
