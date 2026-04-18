from typing import Optional, Union

from pydantic import Field

from ...base import ConfiguredBaseModel
from .field_data import (
    SerializedDictFieldData,
    SerializedGenericData,
    SerializedTableFieldData,
)

__all__ = ["SerializedExtractedField"]


FieldDataType = Union[
    SerializedGenericData,
    list[SerializedGenericData],
    SerializedDictFieldData,
    list[SerializedDictFieldData],
    SerializedTableFieldData,
    list[SerializedTableFieldData],
]


class SerializedExtractedField(ConfiguredBaseModel):
    field_code: str = Field(..., alias="fieldCode")
    data: FieldDataType
    aliases: Optional[dict[str, str]] = None
