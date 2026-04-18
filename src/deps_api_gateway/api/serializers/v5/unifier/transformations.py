from typing import Any

from ...base import ConfiguredBaseModel

__all__ = ["SerializedAppliedTransformation"]


class SerializedTransformationParameters(ConfiguredBaseModel):
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


class SerializedAppliedTransformation(ConfiguredBaseModel):
    name: str
    parameters: SerializedTransformationParameters
