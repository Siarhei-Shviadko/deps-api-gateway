from pydantic import Field

from ...base import ConfiguredBaseModel
from .extracted_field import SerializedExtractedField
from .group import SerializedGroup

__all__ = ["SerializedExtractedData"]


class SerializedExtractedData(ConfiguredBaseModel):
    document_id: int = Field(..., alias="documentId")
    fields: list[SerializedExtractedField]
    groups: list[SerializedGroup]
