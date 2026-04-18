from typing import Optional

from ...base import ConfiguredBaseModel

__all__ = ["CreatePrototypeRequest", "CreatePrototypeResponse"]


class CreatePrototypeRequest(ConfiguredBaseModel):
    name: str
    engine: str
    language: str
    description: Optional[str] = None


class CreatePrototypeResponse(ConfiguredBaseModel):
    id: str
