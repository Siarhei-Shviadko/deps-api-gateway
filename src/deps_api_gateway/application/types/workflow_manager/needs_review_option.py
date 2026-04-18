from enum import Enum

__all__ = ["NeedsReviewOption"]


class NeedsReviewOption(str, Enum):
    ALWAYS_REVIEW = "always_review"
    REVIEW_IF_VALIDATION_FAILURE = "review_if_validation_failure"
    NO_REVIEW = "no_review"
