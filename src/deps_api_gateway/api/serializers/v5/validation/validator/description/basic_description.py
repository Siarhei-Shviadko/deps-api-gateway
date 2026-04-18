from typing import Any, Optional

from .....base import ConfiguredBaseModel

__all__ = ["BasicDescription"]


class BasicDescription(ConfiguredBaseModel):
    allowed_values: Optional[list[Any]]
    restricted_values: Optional[list[Any]]
