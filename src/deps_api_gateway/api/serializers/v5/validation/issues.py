from typing import Optional

from pydantic import Field

from ...base import ConfiguredBaseModel
from .cross_field_issue import SerializedCrossFieldIssue
from .issue import SerializedIssue

__all__ = ["SerializedIssues"]


class SerializedIssues(ConfiguredBaseModel):
    field_code: str = Field(..., alias="fieldCode")
    document_id: str = Field(..., alias="documentId")
    errors: Optional[list[SerializedIssue]]
    warnings: Optional[list[SerializedIssue]]
    cross_field_errors: Optional[list[SerializedCrossFieldIssue]] = Field(alias="crossFieldErrors")
    cross_field_warnings: Optional[list[SerializedCrossFieldIssue]] = Field(alias="crossFieldWarnings")
