import uuid
from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    HIGH_SPARROW_BASE_PREFIX,
    V1_PREFIX,
)
from tests.data.validation_json_data import (
    GET_ALL_VALIDATORS_RESPONSE_DICT,
    GET_ALL_VALIDATORS_RESPONSE_JSON,
    HIGH_SPARROW_CREATE_RULE_DICT,
    HIGH_SPARROW_CREATE_RULE_JSON,
    HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_DICT,
    HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_JSON,
    HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_DICT,
    HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_JSON,
    HIGH_SPARROW_VALIDATE_FIELD_OK_DICT,
    HIGH_SPARROW_VALIDATE_FIELD_OK_JSON,
    HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_DICT,
    HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_JSON,
    HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_DICT,
    HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_JSON,
    HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT,
    HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON,
)

HIGH_SPARROW_BASE_URL = f"{HIGH_SPARROW_BASE_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.validation
async def test_get_validation_result__ok__not_valid(client, document_id):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/results/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(high_sparrow_url, body=HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/validation-result")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == HIGH_SPARROW_VALIDATION_RESULTS_NOT_VALID_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_get_validation_result__ok__valid(client, document_id):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/results/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(high_sparrow_url, body=HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/validation-result")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_get_validation_result__not_found(client, document_id):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/results/{document_id}"
    with aioresponses() as mock_response:
        mock_response.get(
            high_sparrow_url, status=HTTPStatus.NOT_FOUND, body=HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_JSON
        )

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/validation-result")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == HIGH_SPARROW_VALIDATION_RESULTS_NOT_FOUND_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_attach_validator__created(
    client,
    document_type_id,
    external_validator_name,
    external_validator_url,
):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/external-validators"
    data = {"name": external_validator_name, "url": external_validator_url}
    with aioresponses() as mock_response:
        mock_response.post(url=high_sparrow_url, status=HTTPStatus.CREATED)

        response = await client.post(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/external-validators",
            json=data,
        )

        assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
@pytest.mark.validation
async def test_remove_validator__no_content(
    client,
    document_type_id,
    external_validator_name,
):
    high_sparrow_url = (
        f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/external-validators/{external_validator_name}"
    )
    with aioresponses() as mock_response:
        mock_response.delete(url=high_sparrow_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/"
            f"external-validators/{external_validator_name}",
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_create_rule__created(
    client,
    document_type_id,
    validator_code,
    validation_rule_name,
):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/validators/{validator_code}/rules"
    data = {
        "name": validation_rule_name,
        "severity": "error",
        "rule": uuid.uuid4().hex,
        "issue_message": uuid.uuid4().hex,
        "description": uuid.uuid4().hex,
        "need_warning_even_if_optional": False,
        "for_each": False,
        "for_any": False,
        "check_optional_fields": False,
    }

    with aioresponses() as mock_response:
        mock_response.post(url=high_sparrow_url, status=HTTPStatus.CREATED, body=HIGH_SPARROW_CREATE_RULE_JSON)

        response = await client.post(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/rules",
            json=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == HIGH_SPARROW_CREATE_RULE_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_delete_rule__no_content(
    client,
    document_type_id,
    validator_code,
    validation_rule_name,
):
    high_sparrow_url = (
        f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/validators/{validator_code}"
        f"/rules/{validation_rule_name}"
    )
    with aioresponses() as mock_response:
        mock_response.delete(url=high_sparrow_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators/{validator_code}"
            f"/rules/{validation_rule_name}"
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_update_cross_field_validator__no_content(
    client,
    document_type_id,
    validator_code,
):
    high_sparrow_url = (
        f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/cross-field-validators/{validator_code}"
    )
    data = {
        "name": "test",
        "description": "",
        "rule": "testrule",
        "severity": "warning",
        "validated_fields": [],
        "issue_message": "message",
        "dependent_fields": [],
        "for_each": False,
        "for_any": False,
    }

    with aioresponses() as mock_response:
        mock_response.patch(url=high_sparrow_url, status=HTTPStatus.OK)

        response = await client.patch(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/cross-field-validators/{validator_code}",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.validation
async def test_get_all_validators__ok(client, document_type_id: str):
    url = f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/validators"

    with aioresponses() as mock_response:
        mock_response.get(url, body=GET_ALL_VALIDATORS_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.get(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_ALL_VALIDATORS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_validate_field__ok(client, document_type_id, validator_code, document_id):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/validators/{validator_code}/validate"
    data = {"documentId": document_id}

    with aioresponses() as mock_response:
        mock_response.post(url=high_sparrow_url, status=HTTPStatus.OK, body=HIGH_SPARROW_VALIDATE_FIELD_OK_JSON)

        response = await client.post(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/validate",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == HIGH_SPARROW_VALIDATE_FIELD_OK_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_validate_field__not_valid(client, document_type_id, validator_code, document_id):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/validators/{validator_code}/validate"
    data = {"documentId": document_id}

    with aioresponses() as mock_response:
        mock_response.post(url=high_sparrow_url, status=HTTPStatus.OK, body=HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_JSON)

        response = await client.post(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/validate",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == HIGH_SPARROW_VALIDATE_FIELD_NOT_VALID_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_validate_field__not_found(client, document_type_id, validator_code, document_id):
    high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/document-types/{document_type_id}/validators/{validator_code}/validate"
    data = {"documentId": document_id}

    with aioresponses() as mock_response:
        mock_response.post(
            url=high_sparrow_url,
            status=HTTPStatus.NOT_FOUND,
            body=HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_JSON,
        )

        response = await client.post(
            url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/validate",
            json=data,
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == HIGH_SPARROW_VALIDATE_FIELD_NOT_FOUND_DICT


@pytest.mark.asyncio
@pytest.mark.validation
async def test_validate_field__missing_document_id(client, document_type_id, validator_code):
    response = await client.post(
        url=f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/validators/{validator_code}/validate",
        json={},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
