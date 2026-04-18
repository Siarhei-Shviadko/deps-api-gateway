from pydantic import AnyHttpUrl

from ...base import ConfiguredBaseModel

__all__ = ["SerializedExternalValidator"]


class SerializedExternalValidator(ConfiguredBaseModel):
    name: str
    url: AnyHttpUrl
