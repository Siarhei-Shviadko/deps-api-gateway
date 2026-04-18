from typing import List, Optional

from .....base import ConfiguredBaseModel
from ..point import SerializedPoint

__all__ = ["SerializedKeyValuePairElementUpdateData", "UpdateKeyValuePairRequest"]


class SerializedKeyValuePairElementUpdateData(ConfiguredBaseModel):
    content: Optional[str] = None
    polygon: Optional[List[SerializedPoint]] = None


class UpdateKeyValuePairRequest(ConfiguredBaseModel):
    key: Optional[SerializedKeyValuePairElementUpdateData] = None
    value: Optional[SerializedKeyValuePairElementUpdateData] = None
