from typing import Optional, TypedDict, Union

from .dict_field_data import DictFieldData
from .generic_data import GenericData
from .table_field_data import TableFieldData

__all__ = ["ExtractedFieldData"]


FieldDataType = Union[
    GenericData,
    list[GenericData],
    DictFieldData,
    list[DictFieldData],
    TableFieldData,
    list[TableFieldData],
]


class ExtractedFieldData(TypedDict, total=False):
    fieldCode: str
    data: FieldDataType
    aliases: Optional[dict[str, str]]
