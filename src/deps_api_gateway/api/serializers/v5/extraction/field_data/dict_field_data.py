from typing import Optional

from ....base import ConfiguredBaseModel
from .generic_data import SerializedGenericData

__all__ = ["SerializedDictFieldData"]


class SerializedDictFieldData(ConfiguredBaseModel):
    id: Optional[str] = None
    key: SerializedGenericData
    value: SerializedGenericData
