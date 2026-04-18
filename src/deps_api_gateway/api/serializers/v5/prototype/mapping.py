from pydantic import Field

from deps_api_gateway.application import MappingType, PrototypeDataTypeCode

from ...base import ConfiguredBaseModel

__all__ = ["CreateMappingRequest", "ModifyMappingRequest", "SerializedMapping"]


class SerializedMapping(ConfiguredBaseModel):
    code: str = Field(..., description="Mapping code equal to the Field Code this Mapping belongs to.")
    prototype_id: str = Field(..., alias="prototypeId")
    keys: list[str]
    data_type: PrototypeDataTypeCode = Field(..., alias="dataType")
    mapping_type: MappingType = Field(..., alias="mappingType")


class CreateMappingRequest(ConfiguredBaseModel):
    code: str = Field(..., description="Mapping code equal to the Field Code this Mapping belongs to.")
    data_type: PrototypeDataTypeCode = Field(..., alias="typeCode")
    keys: list[str]
    mapping_type: MappingType = Field(..., alias="mappingType")


class ModifyMappingRequest(ConfiguredBaseModel):
    keys: list[str]
