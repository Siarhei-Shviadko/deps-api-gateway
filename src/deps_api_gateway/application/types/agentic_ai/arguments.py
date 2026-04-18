from typing import TypeAlias, TypedDict

__all__ = ["ContextArguments", "ArgumentData"]


class ArgumentData(TypedDict):
    parameter: str
    value: str


ContextArguments: TypeAlias = dict[str, dict[str, list[ArgumentData]]]
