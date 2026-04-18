from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .transformations import SerializedAppliedTransformation

__all__ = ["SerializedImage"]


class SerializedImage(ConfiguredBaseModel):
    id: str
    page: int
    blob_name: str = Field(..., alias="blobName")
    width: int
    height: int
    applied_transformation: Optional[SerializedAppliedTransformation] = Field(None, alias="appliedTransformation")
    original_image_id: Optional[str] = Field(None, alias="originalImageId")
