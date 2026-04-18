from deps_api_gateway.application.types import Severity

from ...base import ConfiguredBaseModel

__all__ = ["SerializedRule"]


class SerializedRule(ConfiguredBaseModel):
    name: str
    severity: Severity
    rule: str
    issue_message: str
    description: str
    need_warning_even_if_optional: bool
    for_each: bool
    for_any: bool
    check_optional_fields: bool
