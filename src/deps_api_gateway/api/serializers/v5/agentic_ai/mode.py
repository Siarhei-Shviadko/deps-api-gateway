from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["ParameterSerializer", "ToolSerializer", "ToolSetSerializer", "ModeSerializer", "GetModesResponse"]


class ParameterSerializer(ConfiguredBaseModel):
    name: str


class ToolSerializer(ConfiguredBaseModel):
    code: str
    name: str
    parameters: list[ParameterSerializer]  # noqa: WPS110


class ToolSetSerializer(ConfiguredBaseModel):
    id: str
    code: str
    name: str
    tools: list[ToolSerializer]


class ModeSerializer(ConfiguredBaseModel):
    id: str
    code: str
    tool_sets: list[ToolSetSerializer] = Field(..., alias="toolSets")


class GetModesResponse(ConfiguredBaseModel):
    modes: list[ModeSerializer]
