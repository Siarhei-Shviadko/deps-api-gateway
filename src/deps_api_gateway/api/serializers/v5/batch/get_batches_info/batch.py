from datetime import datetime
from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel
from .file import SerializedListBatchFileInfo

__all__ = ["SerializedListBatchInfo"]


class SerializedListBatchInfo(ConfiguredBaseModel):
    id: str
    name: str
    group: Optional[str]
    status: str
    files: list[SerializedListBatchFileInfo]
    created_at: datetime = Field(..., alias="createdAt")
