from datetime import datetime
from typing import Optional

from ...base import ConfiguredBaseModel

__all__ = [
    "BoundingBoxResponse",
    "ContentRegionResponse",
    "SplitSegmentResponse",
    "GetProposalResponse",
]


class BoundingBoxResponse(ConfiguredBaseModel):
    x: float
    y: float
    width: float
    height: float


class ContentRegionResponse(ConfiguredBaseModel):
    page_number: int
    bounding_box: Optional[BoundingBoxResponse] = None


class SplitSegmentResponse(ConfiguredBaseModel):
    name: str
    content_regions: list[ContentRegionResponse]
    document_type_id: Optional[str] = None


class GetProposalResponse(ConfiguredBaseModel):
    id: str
    tenant_id: str
    group_id: str
    document_type_id: Optional[str] = None
    status: str
    batch_name: str
    segments: list[SplitSegmentResponse]
    total_pages: int
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
