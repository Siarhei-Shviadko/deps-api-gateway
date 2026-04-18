from typing import Optional, TypedDict

from .generic_data import GenericData

__all__ = ["DictFieldData"]


class DictFieldData(TypedDict, total=False):
    id: Optional[str]
    key: GenericData
    value: GenericData
