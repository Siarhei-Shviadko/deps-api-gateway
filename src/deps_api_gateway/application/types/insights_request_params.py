from typing import Optional, TypedDict

__all__ = ["InsightsRequestParamsDict"]


class InsightsRequestParamsDictBase(TypedDict, total=True):
    temperature: float
    top_p: float


class InsightsRequestParamsDict(InsightsRequestParamsDictBase, total=False):
    groupingFactor: Optional[int]
    pageSpan: Optional[tuple[int, int]]
