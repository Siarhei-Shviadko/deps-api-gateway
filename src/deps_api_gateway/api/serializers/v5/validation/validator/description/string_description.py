from .....base import ConfiguredBaseModel

__all__ = ["StringDescription"]


class StringDescription(ConfiguredBaseModel):
    max_length: int
