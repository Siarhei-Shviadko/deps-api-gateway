from .....base import ConfiguredBaseModel

__all__ = ["SerializedGroup"]


class SerializedGroup(ConfiguredBaseModel):
    id: str
    name: str
    members: set[str]
