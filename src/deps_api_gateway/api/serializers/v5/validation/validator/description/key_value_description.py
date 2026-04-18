from .....base import ConfiguredBaseModel
from ..operand_type import OperandType
from .generic_description import GenericDescription

__all__ = ["KeyValueDescription"]


class KeyValueDescription(ConfiguredBaseModel):
    key_type: OperandType
    key_meta: GenericDescription
    value_type: OperandType
    value_meta: GenericDescription
