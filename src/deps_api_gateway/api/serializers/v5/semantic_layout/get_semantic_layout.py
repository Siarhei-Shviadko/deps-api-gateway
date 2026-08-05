from datetime import datetime

from pydantic import Field

from ...base import ConfiguredBaseModel
from .content_serializers import (
    SerializedImageContent,
    SerializedListContent,
    SerializedParagraphContent,
    SerializedTableContent,
)

__all__ = [
    "SerializedSemanticMetadata",
    "SerializedContentElement",
    "SerializedSection",
    "SerializedSemanticLayout",
]


class SerializedSemanticMetadata(ConfiguredBaseModel):
    source_provider: str = Field(..., alias="sourceProvider")
    processing_time_ms: int | None = Field(None, alias="processingTimeMs")
    confidence: float | None = None


class SerializedContentElement(ConfiguredBaseModel):
    id: str
    order: int
    type: str
    content: (SerializedParagraphContent | SerializedListContent | SerializedTableContent | SerializedImageContent)


class SerializedSection(ConfiguredBaseModel):
    id: str
    order: int
    title: str | None = None
    content_elements: list[SerializedContentElement] = Field(..., alias="contentElements")


class SerializedSemanticLayout(ConfiguredBaseModel):
    id: str
    created_at: datetime = Field(..., alias="createdAt")
    metadata: SerializedSemanticMetadata
    sections: list[SerializedSection]
