from typing import Optional

from ....base import ConfiguredBaseModel

__all__ = ["SerializedListBatchFileInfo"]


class SerializedListBatchFileInfo(ConfiguredBaseModel):
    name: str
    status: str
    error: Optional[str]
