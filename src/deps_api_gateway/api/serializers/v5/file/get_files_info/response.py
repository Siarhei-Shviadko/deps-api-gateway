from pydantic import Field

from ....base import ConfiguredBaseModel
from .file import SerializedFileInfo
from .paginated_result_metadata import PaginatedResultMetadata

__all__ = ["GetFilesInfoResponse"]


class GetFilesInfoResponse(ConfiguredBaseModel):
    metadata: PaginatedResultMetadata = Field(..., alias="meta")
    files: list[SerializedFileInfo] = Field(..., alias="result")
