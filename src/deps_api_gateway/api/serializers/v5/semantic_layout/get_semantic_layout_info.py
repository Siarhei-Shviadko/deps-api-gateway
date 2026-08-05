from datetime import datetime

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = [
    "SerializedSemanticLayoutParsingMetadata",
    "SerializedSemanticLayoutInfo",
    "SerializedAllSemanticLayoutInfo",
]


class SerializedSemanticLayoutParsingMetadata(ConfiguredBaseModel):
    source_provider: str = Field(..., alias="sourceProvider")
    processing_time_ms: int | None = Field(None, alias="processingTimeMs")
    confidence: float | None = None


class SerializedSemanticLayoutInfo(ConfiguredBaseModel):
    id: str
    provider: str
    created_at: datetime = Field(..., alias="createdAt")
    metadata: SerializedSemanticLayoutParsingMetadata


class SerializedAllSemanticLayoutInfo(ConfiguredBaseModel):
    layout_id: str = Field(..., alias="layoutId")
    semantic_layout_info: dict[str, SerializedSemanticLayoutInfo] = Field(..., alias="semanticLayoutInfo")
