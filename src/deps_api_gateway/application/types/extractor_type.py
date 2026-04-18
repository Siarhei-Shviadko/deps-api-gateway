from enum import Enum

__all__ = ["ExtractorType"]


class ExtractorType(str, Enum):
    PLUGIN = "plugin"
    TEMPLATE = "template"
    PROTOTYPE = "prototype"
    NON = "non"
