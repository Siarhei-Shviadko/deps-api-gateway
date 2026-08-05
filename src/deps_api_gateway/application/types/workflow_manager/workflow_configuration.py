from typing import TypedDict

from ...parsing import ParsingFeature
from .needs_review_option import NeedsReviewOption

__all__ = ["WorkflowConfiguration"]


class WorkflowConfiguration(TypedDict):
    document_type_id: str
    parsing_features: list[ParsingFeature] | None
    needs_postprocessing: bool | None
    needs_extraction: bool | None
    needs_validation: bool | None
    needs_review: NeedsReviewOption | None
    needs_output_exporting: bool | None
    engine: str | None
