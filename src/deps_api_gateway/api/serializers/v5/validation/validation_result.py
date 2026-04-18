from pydantic import Field

from ...base import ConfiguredBaseModel
from .issues import SerializedIssues

__all__ = ["SerializedValidationResult"]


class SerializedValidationResult(ConfiguredBaseModel):
    is_valid: bool = Field(..., alias="isValid")
    detail: list[SerializedIssues]
