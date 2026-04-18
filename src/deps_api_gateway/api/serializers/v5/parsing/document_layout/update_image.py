from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel
from .point import SerializedPoint

__all__ = ["UpdateImageRequest"]


class UpdateImageRequest(ConfiguredBaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    filepath: Optional[str] = None
    polygon: list[SerializedPoint] = Field(default_factory=list)
