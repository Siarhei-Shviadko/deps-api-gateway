from typing import TypedDict

__all__ = ["SourceTextCoordinatesData", "CharRangeData"]


class CharRangeData(TypedDict):
    begin: int
    end: int


class SourceTextCoordinatesData(TypedDict):
    sourceId: str
    charRanges: list[CharRangeData]
