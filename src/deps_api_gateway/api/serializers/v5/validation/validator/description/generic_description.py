from typing import Union

from .basic_description import BasicDescription
from .date_description import DateDescription
from .enum_description import EnumDescription
from .string_description import StringDescription

__all__ = ["GenericDescription"]


GenericDescription = Union[
    BasicDescription,
    StringDescription,
    EnumDescription,
    DateDescription,
]
