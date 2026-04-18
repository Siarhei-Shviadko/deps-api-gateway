from ...base import ConfiguredBaseModel
from .extra_data import SerializedExtraData

__all__ = ["SerializedSupplement"]


class SerializedSupplement(ConfiguredBaseModel):
    data: list[SerializedExtraData]
