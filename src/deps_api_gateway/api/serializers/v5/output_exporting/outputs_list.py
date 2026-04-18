from ...base import ConfiguredBaseModel
from .output import SerializedOutput

__all__ = ["OutputsListResponse"]


class OutputsListResponse(ConfiguredBaseModel):
    outputs: list[SerializedOutput]
