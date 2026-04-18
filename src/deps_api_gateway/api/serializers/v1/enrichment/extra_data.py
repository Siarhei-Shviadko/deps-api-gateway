from typing import Optional

from ...base import ConfiguredBaseModel

__all__ = ["SerializedExtraData"]


class SerializedExtraData(ConfiguredBaseModel):
    name: str
    value: str
    code: Optional[str] = None
