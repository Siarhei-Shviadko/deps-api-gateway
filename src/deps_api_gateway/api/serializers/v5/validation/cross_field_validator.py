from typing import List, Optional

from deps_api_gateway.application import Severity

from ...base import ConfiguredBaseModel

__all__ = [
    "SerializedCrossFieldValidator",
    "UpdateCrossFieldValidatorRequest",
    "UpdateCrossFieldValidatorResponse",
    "CreateCrossFieldValidatorRequest",
]


class SerializedCrossFieldIssueMessage(ConfiguredBaseModel):
    message: str
    dependent_fields: List[str]


class SerializedCrossFieldValidator(ConfiguredBaseModel):
    id: str
    name: str
    description: str
    rule: str
    severity: Severity
    validated_fields: List[str]
    issue_message: SerializedCrossFieldIssueMessage
    for_each: bool
    for_any: bool


class CreateCrossFieldValidatorRequest(ConfiguredBaseModel):
    name: str
    description: Optional[str] = ""
    rule: str
    severity: Severity
    validated_fields: List[str]
    issue_message: str
    dependent_fields: List[str]
    for_each: Optional[bool] = False
    for_any: Optional[bool] = False


class UpdateCrossFieldValidatorRequest(ConfiguredBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rule: Optional[str] = None
    severity: Optional[Severity] = None
    validated_fields: Optional[list[str]] = None
    issue_message: Optional[str] = None
    dependent_fields: Optional[list[str]] = None
    for_each: Optional[bool] = None
    for_any: Optional[bool] = None


class UpdateCrossFieldValidatorResponse(ConfiguredBaseModel):
    id: str
