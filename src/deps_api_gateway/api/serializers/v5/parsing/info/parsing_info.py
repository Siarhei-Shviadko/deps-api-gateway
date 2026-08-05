from typing import Optional

from pydantic import Field

from ....base import ConfiguredBaseModel
from ...semantic_layout.get_semantic_layout_info import SerializedSemanticLayoutInfo
from .dl_info import SerializedDocumentLayoutInfo
from .tl_info import SerializerTabularLayoutInfo

__all__ = ["SerializedParsingInfo"]


class SerializedParsingInfo(ConfiguredBaseModel):
    layout_id: str = Field(..., alias="layoutId")
    document_layout_info: Optional[SerializedDocumentLayoutInfo] = Field(..., alias="documentLayoutInfo")
    tabular_layout_info: Optional[SerializerTabularLayoutInfo] = Field(..., alias="tabularLayoutInfo")
    semantic_layout_info: Optional[dict[str, SerializedSemanticLayoutInfo]] = Field(None, alias="semanticLayoutInfo")
