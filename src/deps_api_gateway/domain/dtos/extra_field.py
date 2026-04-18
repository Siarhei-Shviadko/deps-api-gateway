from dataclasses import dataclass

__all__ = ["ExtraFieldData"]


@dataclass
class ExtraFieldData:
    code: str
    name: str
    display_order: int
