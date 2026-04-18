from typing import TypedDict

from .field_data import ExtractedFieldData
from .group_data import GroupData

__all__ = ["SaveExtractedDataDTO"]


class SaveExtractedDataDTO(TypedDict, total=False):
    fields: list[ExtractedFieldData]
    groups: list[GroupData]
