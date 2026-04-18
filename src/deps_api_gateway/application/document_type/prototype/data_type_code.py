from enum import Enum

__all__ = ["PrototypeDataTypeCode"]


class PrototypeDataTypeCode(str, Enum):
    TABLE = "table"
    STRING = "string"
    CHECKMARK = "checkmark"
    ENUM = "enum"
    DATE = "date"
    NUMERIC = "numeric"
