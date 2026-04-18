from .....base import ConfiguredBaseModel

__all__ = ["DateDescription"]


class DateDescription(ConfiguredBaseModel):
    format: str
