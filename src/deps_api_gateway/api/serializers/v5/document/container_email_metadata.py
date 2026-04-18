from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedContainerEmailMetadata"]


class SerializedContainerEmailMetadata(ConfiguredBaseModel):
    first_level_child_count: Optional[int] = Field(1, alias="firstLevelChildCount")
    subject: Optional[str] = None
    sender: Optional[str] = None
    recipients: Optional[list[str]] = None
    cc: Optional[list[str]] = None
    body: Optional[str] = None
    date: Optional[str] = None
