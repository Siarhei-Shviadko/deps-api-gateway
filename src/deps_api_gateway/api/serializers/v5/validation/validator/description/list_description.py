from typing import Union

from .....base import ConfiguredBaseModel
from ..operand_type import OperandType
from .generic_description import GenericDescription
from .key_value_description import KeyValueDescription
from .table_description import TableDescription

__all__ = ["ListDescription"]


ListType = Union[
    GenericDescription,
    KeyValueDescription,
    TableDescription,
]


class ListDescription(ConfiguredBaseModel):
    item_type: OperandType
    meta: ListType
