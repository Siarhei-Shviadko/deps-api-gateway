from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SaveSupplementRequest", "SaveSupplementResponse", "SerializedSaveExtraDataElement"]


class SerializedSaveExtraDataElement(ConfiguredBaseModel):
    name: str
    value: str
    code: Optional[str] = None


class SaveSupplementRequest(ConfiguredBaseModel):
    data: list[SerializedSaveExtraDataElement]
    document_type_id: Optional[str] = Field(..., alias="documentTypeId")


class SaveSupplementResponse(ConfiguredBaseModel):
    entity_id: str = Field(..., alias="entityId")
