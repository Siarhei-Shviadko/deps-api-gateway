from ....base import ConfiguredBaseModel
from .label import SerializedLabel

__all__ = ["GetLabelsResponse"]


class GetLabelsResponse(ConfiguredBaseModel):
    labels: list[SerializedLabel]
