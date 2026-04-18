from typing import Optional

from async_rest_client import Methods

from deps_api_gateway.application import (
    IHighSparrowProxy,
    ProxyResponse,
    ProxyResponseFactory,
    Severity,
)
from deps_api_gateway.constants import HIGH_SPARROW_BASE_PREFIX, V1_PREFIX

from ..generic_rest_client import GenericRestClient
from .exceptions import HighSparrowError, HighSparrowServiceUnavailableError

__all__ = ["HighSparrowProxy"]


class HighSparrowProxy(GenericRestClient, IHighSparrowProxy):
    v1_prefix = f"{HIGH_SPARROW_BASE_PREFIX}{V1_PREFIX}"
    exception = HighSparrowError

    async def get_validation_result(self, entity_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/results/{entity_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

    async def attach_validator(
        self, document_type_id: str, external_validator_name: str, external_validator_url: str
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/external-validators"

        data = {
            "name": external_validator_name,
            "url": external_validator_url,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

    async def remove_validator(self, document_type_id: str, external_validator_name: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/external-validators/{external_validator_name}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

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
        url = f"{self.v1_prefix}/document-types/{document_type_id}/validators/{validator_code}/rules"

        data = {
            "name": name,
            "severity": severity,
            "rule": rule,
            "issueMessage": issue_message,
            "description": description,
            "needWarningEvenIfOptional": need_warning_even_if_optional,
            "forEach": for_each,
            "forAny": for_any,
            "checkOptionalFields": check_optional_fields,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

    async def delete_rule(
        self,
        document_type_id: str,
        validator_code: str,
        rule_name: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/validators/{validator_code}/rules/{rule_name}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

    async def find_document_type(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}"

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

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
        url = f"{self.v1_prefix}/document-types/{document_type_id}/cross-field-validators"

        data = {
            "name": name,
            "description": description,
            "rule": rule,
            "severity": severity,
            "validatedFields": validated_fields,
            "issueMessage": issue_message,
            "dependentFields": dependent_fields,
            "forEach": for_each,
            "forAny": for_any,
        }

        try:
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
        except Exception as error:
            raise HighSparrowServiceUnavailableError(error)

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
        url = f"{self.v1_prefix}/document-types/{document_type_id}/cross-field-validators/{validator_id}"

        data = {
            "name": name,
            "description": description,
            "rule": rule,
            "severity": severity,
            "validatedFields": validated_fields,
            "issueMessage": issue_message,
            "dependentFields": dependent_fields,
            "forEach": for_each,
            "forAny": for_any,
        }

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.PATCH, url=url, json=data))

    async def delete_cross_field_validator(
        self,
        document_type_id: str,
        validator_id: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/cross-field-validators/{validator_id}"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.DELETE, url=url))

    async def get_all_validators(self, document_type_id: str) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/validators"

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.GET, url=url))

    async def validate_field(
        self,
        document_type_id: str,
        validator_code: str,
        document_id: str,
    ) -> ProxyResponse:
        url = f"{self.v1_prefix}/document-types/{document_type_id}/validators/{validator_code}/validate"

        data = {"documentId": document_id}

        async with self._handling_exception():
            return ProxyResponseFactory.make_response_from(await self.request(method=Methods.POST, url=url, json=data))
