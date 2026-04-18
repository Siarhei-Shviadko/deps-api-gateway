from typing import Optional, Union

from ....base import ConfiguredBaseModel
from .description import (
    BasicDescription,
    DateDescription,
    EnumDescription,
    KeyValueDescription,
    ListDescription,
    StringDescription,
    TableDescription,
)
from .operand_type import OperandType

__all__ = ["ValidatorType"]


DescriptionType = Union[
    StringDescription,
    EnumDescription,
    DateDescription,
    KeyValueDescription,
    ListDescription,
    TableDescription,
    BasicDescription,
]


class ValidatorType(ConfiguredBaseModel):
    type: OperandType
    description: Optional[DescriptionType]
