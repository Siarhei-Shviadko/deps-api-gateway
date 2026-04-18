from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path, Response, status

from deps_api_gateway.application import DocumentTypeService
from deps_api_gateway.constants import DOCUMENT_TYPE_ROUTER_PREFIX
from deps_api_gateway.containers import Application

from ....serializers import (
    CreateCrossFieldValidatorRequest,
    CreateRuleRequest,
    GetAllValidatorsResponse,
    SerializedExternalValidator,
    SerializedRule,
    UpdateCrossFieldValidatorRequest,
    UpdateCrossFieldValidatorResponse,
    ValidateFieldRequest,
)
from ....utilities import ResponseBuilder

__all__ = ["validation_router"]

validation_router = APIRouter(prefix=DOCUMENT_TYPE_ROUTER_PREFIX, tags=["Data Validation"])


@validation_router.get(
    "/{documentTypeId}/validators",
    status_code=status.HTTP_200_OK,
    response_model=GetAllValidatorsResponse,
    description="""
    Returns all types of validators of a document type: basic validators, external validators, cross field validators
    """,
)
@inject
async def get_all_validators(
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.get_all_validators(document_type_id)
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.post(
    "/{documentTypeId}/external-validators", status_code=status.HTTP_201_CREATED, response_class=Response
)
@inject
async def attach_validator(
    external_validator_data: SerializedExternalValidator,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.attach_validator(
        document_type_id=document_type_id,
        external_validator_name=external_validator_data.name,
        external_validator_url=external_validator_data.url,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.delete(
    "/{documentTypeId}/external-validators/{name}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
@inject
async def remove_validator(
    name: str,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.remove_validator(
        document_type_id=document_type_id,
        external_validator_name=name,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.post(
    "/{documentTypeId}/validators/{validatorCode}/rules",
    status_code=status.HTTP_201_CREATED,
    response_model=SerializedRule,
)
@inject
async def create_rule(
    rule_data: CreateRuleRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_code: str = Path(..., alias="validatorCode"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.create_rule(
        document_type_id=document_type_id,
        validator_code=validator_code,
        name=rule_data.name,
        severity=rule_data.severity,
        rule=rule_data.rule,
        issue_message=rule_data.issue_message,
        description=rule_data.description,
        need_warning_even_if_optional=rule_data.need_warning_even_if_optional,
        for_each=rule_data.for_each,
        for_any=rule_data.for_any,
        check_optional_fields=rule_data.check_optional_fields,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.delete(
    "/{documentTypeId}/validators/{validatorCode}/rules/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_rule(
    name: str,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_code: str = Path(..., alias="validatorCode"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_rule(
        document_type_id=document_type_id,
        validator_code=validator_code,
        rule_name=name,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.post(
    "/{documentTypeId}/cross-field-validators", status_code=status.HTTP_201_CREATED, response_class=Response
)
@inject
async def attach_cross_field_validator(
    cross_field_validator_data: CreateCrossFieldValidatorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.attach_cross_field_validator(
        document_type_id=document_type_id,
        name=cross_field_validator_data.name,
        description=cross_field_validator_data.description,
        rule=cross_field_validator_data.rule,
        severity=cross_field_validator_data.severity,
        validated_fields=cross_field_validator_data.validated_fields,
        issue_message=cross_field_validator_data.issue_message,
        dependent_fields=cross_field_validator_data.dependent_fields,
        for_each=cross_field_validator_data.for_each,
        for_any=cross_field_validator_data.for_any,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.patch(
    "/{documentTypeId}/cross-field-validators/{validatorId}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    response_model=UpdateCrossFieldValidatorResponse,
)
@inject
async def update_cross_field_validator(
    crossfield_validator_data: UpdateCrossFieldValidatorRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_id: str = Path(..., alias="validatorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.update_cross_field_validator(
        validator_id=validator_id,
        document_type_id=document_type_id,
        name=crossfield_validator_data.name,
        description=crossfield_validator_data.description,
        rule=crossfield_validator_data.rule,
        severity=crossfield_validator_data.severity,
        validated_fields=crossfield_validator_data.validated_fields,
        issue_message=crossfield_validator_data.issue_message,
        dependent_fields=crossfield_validator_data.dependent_fields,
        for_each=crossfield_validator_data.for_each,
        for_any=crossfield_validator_data.for_any,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.delete(
    "/{documentTypeId}/cross-field-validators/{validatorId}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
@inject
async def delete_cross_field_validator(
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_id: str = Path(..., alias="validatorId"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.delete_cross_field_validator(
        document_type_id=document_type_id,
        validator_id=validator_id,
    )

    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )


@validation_router.post(
    "/{documentTypeId}/validators/{validatorCode}/validate",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
@inject
async def validate_field(
    request_data: ValidateFieldRequest,
    document_type_id: str = Path(..., alias="documentTypeId"),
    validator_code: str = Path(..., alias="validatorCode"),
    application: DocumentTypeService = Depends(Provide[Application.document_type]),
) -> Response:
    proxy_response = await application.validate_field(
        document_type_id=document_type_id,
        validator_code=validator_code,
        document_id=request_data.document_id,
    )
    return (
        ResponseBuilder()
        .with_status(proxy_response.status_code)
        .with_headers(proxy_response.headers)
        .with_content(proxy_response.content)
        .build()
    )
