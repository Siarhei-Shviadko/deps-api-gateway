from typing import Optional

from deps_api_gateway.api.serializers import ConfiguredBaseModel

__all__ = ["SerializedBorders"]


class SerializedBorders(ConfiguredBaseModel):
    top: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None
