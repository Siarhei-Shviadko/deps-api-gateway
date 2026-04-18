from ...base import ConfiguredBaseModel
from .provider import SerializedProvider

__all__ = ["LLMSResponse"]


class LLMSResponse(ConfiguredBaseModel):
    providers: list[SerializedProvider]
