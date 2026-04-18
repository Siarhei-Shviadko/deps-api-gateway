from ....base import ConfiguredBaseModel

__all__ = ["AddCommendRequest"]


class AddCommendRequest(ConfiguredBaseModel):
    text: str
