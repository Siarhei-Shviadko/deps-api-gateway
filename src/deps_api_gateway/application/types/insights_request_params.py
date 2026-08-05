from typing import Any, Optional, TypedDict

__all__ = ["InsightsRequestParamsDict"]


class InsightsRequestParamsDict(TypedDict, total=False):
    temperature: Optional[float]
    top_p: Optional[float]
    max_tokens: Optional[int]
    stop: Optional[list[str]]
    seed: Optional[int]
    logprobs: bool
    extra_model_params: Optional[dict[str, Any]]
    grouping_factor: Optional[int]
    page_span: Optional[dict[str, int]]
