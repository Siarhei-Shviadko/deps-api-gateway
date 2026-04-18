from enum import Enum

__all__ = ["DocumentDetailExtras"]


class DocumentDetailExtras(str, Enum):
    OUTPUTS = "outputs"
    CONVERSATION = "conversation"
    VALIDATION_RESULTS = "validation-results"
    METADATA = "metadata"
    PARSING_INFO = "parsing-info"
