from typing import Optional, TypedDict

__all__ = ["SaveExtraDataElement"]


class SaveExtraDataElement(TypedDict):
    name: str
    value: str
    code: Optional[str]
