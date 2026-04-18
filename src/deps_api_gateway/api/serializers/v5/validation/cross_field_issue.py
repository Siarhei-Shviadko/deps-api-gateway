from typing import Optional

from pydantic import Field

from deps_api_gateway.application.types import Severity

from ...base import ConfiguredBaseModel

__all__ = ["SerializedCrossFieldIssue"]


class SerializedCrossFieldIssue(ConfiguredBaseModel):
    code: str
    validator_id: str = Field(..., alias="validatorId")
    severity: Severity
    validated_fields: list[str] = Field(..., alias="validatedFields")
    message: str

    column: Optional[int]
    row: Optional[int]
    index: Optional[int]
    kv_id: Optional[str] = Field(alias="kvId")
