from enum import Enum

__all__ = ["TemplateDataTypeCode"]


class TemplateDataTypeCode(str, Enum):
    STRING = "string"
    CHECKMARK = "checkmark"
    ENUM = "enum"
    DATE = "date"
    LIST = "list"
    DICT = "dict"
    TABLE = "table"
