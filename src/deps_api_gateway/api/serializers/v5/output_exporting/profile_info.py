from ...base import ConfiguredBaseModel

__all__ = ["ProfileInfoResponse"]


class ProfileInfoResponse(ConfiguredBaseModel):
    id: str
    version: str
