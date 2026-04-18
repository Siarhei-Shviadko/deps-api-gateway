from typing import Optional

from pydantic import Field

from .....base import ConfiguredBaseModel
from ..point import SerializedPoint

__all__ = ["SerializedImage"]


class SerializedImage(ConfiguredBaseModel):
    id: str
    order: int
    title: Optional[str] = None
    file_path: str = Field(alias="filePath")
    polygon: list[SerializedPoint]
    description: Optional[str] = None
