from pydantic import Field

from deps_api_gateway.application.parsing import LayoutType

from ...base import ConfiguredBaseModel

__all__ = ["SerializedEngine", "ParseableEnginesResponse"]


class SerializedEngine(ConfiguredBaseModel):
    code: str
    name: str
    layout_type: LayoutType = Field(..., alias="layoutType")


class ParseableEnginesResponse(ConfiguredBaseModel):
    engines: list[SerializedEngine]
