from typing import Optional

from pydantic import Field

from deps_api_gateway.application import GetGroupExtras

from ...base import ConfiguredBaseModel
from ..splitters import BriefSplitterSerializer
from .classifiers import GenAIClassifierDisplayInfo

__all__ = ["GetGroupResponse"]


class GroupDetailsSerializer(ConfiguredBaseModel):
    id: str
    name: str
    document_type_ids: list[str] = Field(..., alias="documentTypeIds")
    gen_ai_classifiers: Optional[list[GenAIClassifierDisplayInfo]] = Field(
        default=...,
        alias="genAiClassifiers",
        description=f"Optional field, can be requested by passing `extras={GetGroupExtras.CLASSIFIERS.value}`"
        f"query parameter",
    )
    splitters: Optional[list[BriefSplitterSerializer]] = Field(
        default=...,
        alias="splitters",
        description=f"Optional field, can be requested by passing `extras={GetGroupExtras.SPLITTERS.value}`"
        f" query parameter",
    )


class GetGroupResponse(ConfiguredBaseModel):
    group: GroupDetailsSerializer
