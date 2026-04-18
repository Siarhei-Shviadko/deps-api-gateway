from .....base import ConfiguredBaseModel

__all__ = ["EnumDescription"]


class EnumDescription(ConfiguredBaseModel):
    options: list[str]
