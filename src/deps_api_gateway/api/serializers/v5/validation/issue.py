from enum import Enum
from typing import Optional

from pydantic import Field

from deps_api_gateway.application.types import Severity

from ...base import ConfiguredBaseModel

__all__ = ["SerializedIssue"]


class IssueType(Enum):
    PRE_CHECK = "pre_check"
    TYPE_CHECK = "type_check"
    RULES_CHECK = "rules_check"


class SerializedIssue(ConfiguredBaseModel):
    severity: Severity
    type: IssueType
    message: str
    column: Optional[int]
    row: Optional[int]
    index: Optional[int]
    kv_id: Optional[str] = Field(alias="kvId")
