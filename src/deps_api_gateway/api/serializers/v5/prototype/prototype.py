from datetime import datetime
from typing import Any, Optional

from pydantic import Field

from deps_api_gateway.application import FieldType, MappingType, PrototypeDataTypeCode

from ...base import ConfiguredBaseModel
from .header import HeaderType, SerializedHeader
from .layout import SerializedReferenceLayout

__all__ = ["SerializedPrototype"]


class _SerializedFieldType(ConfiguredBaseModel):
    type: FieldType = Field(..., alias="typeCode")
    description: dict[str, Any]


class _SerializedMapping(ConfiguredBaseModel):
    keys: list[str]
    data_type: PrototypeDataTypeCode = Field(..., alias="mappingDataType")
    mapping_type: MappingType = Field(..., alias="mappingType")


class _SerializedTabularMapping(ConfiguredBaseModel):
    headers: list[SerializedHeader] = Field(..., min_length=1)
    header_type: HeaderType = Field(..., alias="headerType")
    occurrence_index: int = Field(0, alias="occurrenceIndex")


class SerializedCompositePrototypeField(ConfiguredBaseModel):
    id: str
    prototype_id: str = Field(..., alias="prototypeId")
    name: str

    field_type: _SerializedFieldType = Field(..., alias="fieldType")
    mapping: _SerializedMapping

    required: bool
    confidential: bool
    read_only: bool = Field(..., alias="readOnly")


class SerializedCompositePrototypeTableField(ConfiguredBaseModel):
    id: str
    prototype_id: str = Field(..., alias="prototypeId")
    name: str

    field_type: _SerializedFieldType = Field(..., alias="fieldType")
    tabular_mapping: _SerializedTabularMapping = Field(..., alias="tabularMapping")

    required: bool
    confidential: bool
    read_only: bool = Field(..., alias="readOnly")


class SerializedPrototype(ConfiguredBaseModel):
    id: str
    name: str
    engine: str
    language: str
    created_at: datetime = Field(..., alias="createdAt")
    description: Optional[str] = None
    fields: list[SerializedCompositePrototypeField]
    table_fields: list[SerializedCompositePrototypeTableField] = Field(..., alias="tableFields")
    reference_layouts: Optional[list[SerializedReferenceLayout]] = Field(..., alias="referenceLayouts")
