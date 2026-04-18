import enum

from pydantic import Field

from ...base import ConfiguredBaseModel

__all__ = ["SerializedProvider", "SerializedLLM"]


class ContextType(str, enum.Enum):
    TEXT_BASED = "text-based"
    BLOB_BASED = "blob-based"


class SerializedLLM(ConfiguredBaseModel):
    code: str
    name: str
    context_type: ContextType = Field(..., alias="contextType")
    description: str


class SerializedProvider(ConfiguredBaseModel):
    code: str
    name: str
    models: list[SerializedLLM]
