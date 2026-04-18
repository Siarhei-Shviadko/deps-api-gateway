from pydantic import Field

from ....base import ConfiguredBaseModel
from .markup import SerializedMarkup

__all__ = ["SerializedReferencePage"]


class SerializedReferencePage(ConfiguredBaseModel):
    id: str
    blob_name: str = Field(..., alias="blobName")
    markups: list[SerializedMarkup] = Field(default_factory=list)
