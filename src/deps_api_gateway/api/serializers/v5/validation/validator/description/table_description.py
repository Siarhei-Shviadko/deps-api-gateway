from .....base import ConfiguredBaseModel
from ..operand_type import OperandType
from .generic_description import GenericDescription

__all__ = ["TableDescription"]


class ColumnDescription(ConfiguredBaseModel):
    index: int
    is_required: bool
    item_type: OperandType
    meta: GenericDescription


class TableDescription(ConfiguredBaseModel):
    columns: list[ColumnDescription]
