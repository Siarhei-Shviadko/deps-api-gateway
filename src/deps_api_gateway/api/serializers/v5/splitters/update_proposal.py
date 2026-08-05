from typing import Optional

from ...base import ConfiguredBaseModel

__all__ = [
    "BoundingBoxRequest",
    "ContentRegionRequest",
    "SplitSegmentRequest",
    "UpdateProposalRequest",
]


class BoundingBoxRequest(ConfiguredBaseModel):
    x: float
    y: float
    width: float
    height: float


class ContentRegionRequest(ConfiguredBaseModel):
    page_number: int
    bounding_box: Optional[BoundingBoxRequest] = None


class SplitSegmentRequest(ConfiguredBaseModel):
    name: str
    content_regions: list[ContentRegionRequest]
    document_type_id: Optional[str] = None


class UpdateProposalRequest(ConfiguredBaseModel):
    segments: list[SplitSegmentRequest]
    batch_name: Optional[str] = None
