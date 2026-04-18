from typing import Optional, Protocol

from ..proxy_response import ProxyResponse
from ..types import Severity

__all__ = ["IHighSparrowProxy"]


class IHighSparrowProxy(Protocol):
    async def get_validation_result(
        self,
        entity_id: str,
    ) -> ProxyResponse:
        ...

    async def attach_validator(
        self,
        document_type_id: str,
        external_validator_name: str,
        external_validator_url: str,
    ) -> ProxyResponse:
        ...

    async def remove_validator(
        self,
        document_type_id: str,
        external_validator_name: str,
    ) -> ProxyResponse:
        ...

    async def create_rule(
        self,
        document_type_id: str,
        validator_code: str,
        name: str,
        severity: Severity,
        rule: str,
        issue_message: str,
        description: str,
        need_warning_even_if_optional: bool,
        for_each: bool,
        for_any: bool,
        check_optional_fields: bool,
    ) -> ProxyResponse:
        ...

    async def delete_rule(
        self,
        document_type_id: str,
        validator_code: str,
        rule_name: str,
    ) -> ProxyResponse:
        ...

    async def find_document_type(self, document_type_id: str) -> ProxyResponse:
        ...

    async def attach_cross_field_validator(
        self,
        document_type_id: str,
        name: str,
        description: str,
        rule: str,
        severity: Severity,
        validated_fields: list[str],
        issue_message: str,
        dependent_fields: list[str],
        for_each: bool = False,
        for_any: bool = False,
    ) -> ProxyResponse:
        ...

    async def update_cross_field_validator(
        self,
        validator_id: str,
        document_type_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        rule: Optional[str] = None,
        severity: Optional[Severity] = None,
        validated_fields: Optional[list[str]] = None,
        issue_message: Optional[str] = None,
        dependent_fields: Optional[list[str]] = None,
        for_each: Optional[bool] = None,
        for_any: Optional[bool] = None,
    ) -> ProxyResponse:
        ...

    async def delete_cross_field_validator(
        self,
        document_type_id: str,
        validator_id: str,
    ) -> ProxyResponse:
        ...

    async def get_all_validators(self, document_type_id: str) -> ProxyResponse:
        ...

    async def validate_field(
        self,
        document_type_id: str,
        validator_code: str,
        document_id: str,
    ) -> ProxyResponse:
        ...
