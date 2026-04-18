from typing import Optional

from deps_api_gateway.api.serializers import ConfiguredBaseModel

__all__ = ["SerializedAlignment"]


class SerializedAlignment(ConfiguredBaseModel):
    horizontal: Optional[str] = None
    vertical: Optional[str] = None
    rotation: Optional[int] = None
