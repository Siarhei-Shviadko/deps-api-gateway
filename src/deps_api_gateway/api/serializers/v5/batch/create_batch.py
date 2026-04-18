from typing import Any, Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .create_file_data import FileRequestSerializer

__all__ = ["CreateBatchRequest", "CreateBatchResponse", "UpdateBatchRequest"]


class CreateBatchRequest(ConfiguredBaseModel):
    name: str
    group_id: Optional[str] = Field(None, alias="groupId")
    metadata: Optional[dict[str, Any]] = Field(None)
    files: list[FileRequestSerializer] = Field(..., alias="files")


class CreateBatchResponse(ConfiguredBaseModel):
    id: str


class UpdateBatchRequest(ConfiguredBaseModel):
    name: str
