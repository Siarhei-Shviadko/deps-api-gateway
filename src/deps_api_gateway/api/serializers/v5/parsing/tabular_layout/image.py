from typing import Optional

from pydantic import Field

from deps_api_gateway.api.serializers import ConfiguredBaseModel

__all__ = ["SerializedImage"]


class SerializedImage(ConfiguredBaseModel):
    id: str
    file_path: str = Field(..., alias="filePath")
    type: str
    position: Optional[tuple[int, int]] = None
    title: Optional[str] = None
    description: Optional[str] = None
