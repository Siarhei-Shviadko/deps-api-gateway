from ...base import ConfiguredBaseModel

__all__ = ["SerializedInvitation"]


class SerializedInvitation(ConfiguredBaseModel):
    email: str
