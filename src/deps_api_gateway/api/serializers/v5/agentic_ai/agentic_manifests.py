from ...base import ConfiguredBaseModel

__all__ = ["RegisterManifestRequest", "RegisterManifestResponse"]


class RegisterManifestRequest(ConfiguredBaseModel):
    code: str
    name: str
    description: str
    url: str
    timeout: int


class RegisterManifestResponse(ConfiguredBaseModel):
    code: str
