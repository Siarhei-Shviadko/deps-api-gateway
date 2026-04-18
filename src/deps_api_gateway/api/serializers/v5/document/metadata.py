from typing import Any

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedDocumentMetadata"]


class SerializedDocumentMetadata(ConfiguredBaseModel):
    document_id: str = Field(..., alias="id")
    metadata: dict[str, Any] = Field(default_factory=dict)
