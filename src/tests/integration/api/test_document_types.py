import uuid
from http import HTTPStatus
from typing import Mapping, Optional
from unittest.mock import AsyncMock, mock_open, patch
from urllib.parse import urlencode

import pytest
from aiohttp.client_exceptions import ClientError
from aioresponses import aioresponses
from httpx import AsyncClient
from multidict import CIMultiDict
from yarl import URL as URL_TYPE

from deps_api_gateway.api.serializers.v1.document_types import DocumentTypeResponseData
from deps_api_gateway.application.document_type import DocumentTypeExtras
from deps_api_gateway.constants import (
    AI_FUSION_BASE_PREFIX,
    API_PREFIX,
    BASE_API_V1_PREFIX,
    BASE_API_V5_PREFIX,
    CLASSIFICATION_BASE_API_PREFIX,
    DOCUMENT_TYPE_BASE_API_PREFIX,
    ENRICHMENT_BASE_PREFIX,
    EXTRACTION_BASE_API_PREFIX,
    HIGH_SPARROW_BASE_PREFIX,
    OUTPUT_EXPORTING_BASE_PREFIX,
    TEMPLATE_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
)
from tests.data.ai_fusion_json_data import (
    AI_FUSION_GET_LLM_EXTRACTORS_RESPONSE_JSON,
    EXPECTED_LLM_EXTRACTORS_IN_DOCUMENT_TYPE_RESPONSE,
)
from tests.data.document_type_json_data import *
from tests.data.enrichment_json_data import (
    EXTRA_FIELDS_RESPONSE_DICT,
    EXTRA_FIELDS_RESPONSE_JSON,
)
from tests.data.extraction_json_data import *
from tests.data.groups_json_data import (
    GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_DICT,
    GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_JSON,
)
from tests.data.json_data import (
    TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
    TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON,
    TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
    TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
    UPDATE_DOCUMENT_TYPE_LLM_RAW_REQUEST,
)
from tests.data.output_exporting_json_data import (
    OUTPUT_PROFILES_RESPONSE_DICT,
    OUTPUT_PROFILES_RESPONSE_JSON,
)
from tests.data.validation_json_data import (
    HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_DICT,
    HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_JSON,
)
from tests.data.workflow_manager_json_data import (
    WORKFLOW_CONFIGURATION_RESPONSE_DICT,
    WORKFLOW_CONFIGURATION_RESPONSE_JSON,
    WORKFLOW_CONFIGURATIONS_RESPONSE_DICT,
    WORKFLOW_CONFIGURATIONS_RESPONSE_JSON,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}
URL = f"{API_PREFIX}/document-types"
DOCUMENT_TYPE_BASE_V1_URL = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V1_PREFIX}"
DOCUMENT_TYPE_BASE_V2_URL = f"{DOCUMENT_TYPE_BASE_API_PREFIX}{V2_PREFIX}"
EXTRACTION_BASE_URL = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}/document-types"
ENRICHMENT_BASE_URL = f"{ENRICHMENT_BASE_PREFIX}{V1_PREFIX}/document-types"
HIGH_SPARROW_BASE_URL = f"{HIGH_SPARROW_BASE_PREFIX}{V1_PREFIX}/document-types"
OUTPUT_EXPORTING_BASE_URL = f"{OUTPUT_EXPORTING_BASE_PREFIX}{V1_PREFIX}/document-types"
TEMPLATE_BASE_BASE_URL = f"{TEMPLATE_BASE_API_PREFIX}{V1_PREFIX}/templates"
WORKFLOW_MANAGER_BASE_BASE_URL = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}"
CLASSIFICATION_BASE_URL = f"{CLASSIFICATION_BASE_API_PREFIX}{V1_PREFIX}"
AI_FUSION_BASE_URL = f"{AI_FUSION_BASE_PREFIX}{V1_PREFIX}"

GENERIC_OLD_REST_CLIENT_PATH = (
    "deps_api_gateway.infrastructure.proxies.generic_rest_client.old.OldGenericRestClient.request"
)
GENERIC_REST_CLIENT_V1_PATH = (
    "deps_api_gateway.infrastructure.proxies.document_type.proxy_v1.DocumentTypeProxyV1.request"
)
GENERIC_REST_CLIENT_V5_PATH = (
    "deps_api_gateway.infrastructure.proxies.document_type.proxy_v5.DocumentTypeProxyV5.request"
)


@pytest.fixture
def mock_types_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": copy.deepcopy(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW),
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": copy.deepcopy(TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW),
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_OLD_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.fixture
def mock_type_request(mocker):
    async_mock = AsyncMock(
        side_effect=[
            {
                "content": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
            {
                "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
                "status_code": 200,
                "headers": HEADERS,
            },
        ]
    )
    mocker.patch(GENERIC_OLD_REST_CLIENT_PATH, side_effect=async_mock)
    return async_mock


@pytest.fixture
def mock_type_response_from_type_service(mocker):
    async_mock = AsyncMock(
        return_value={
            "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
            "status_code": HTTPStatus.OK,
            "headers": HEADERS,
        }
    )
    mocker.patch(GENERIC_REST_CLIENT_V1_PATH, side_effect=async_mock)
    return async_mock


@pytest.fixture
def mock_get_document_types_response_from_type_service(mocker):
    async_mock = AsyncMock(
        return_value={
            "content": DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
            "status_code": HTTPStatus.OK,
            "headers": HEADERS,
        }
    )
    mocker.patch(GENERIC_REST_CLIENT_V1_PATH, side_effect=async_mock)
    return async_mock


@pytest.fixture
def mock_get_document_type_response_from_type_service(mocker):
    async_mock = AsyncMock(
        return_value={
            "content": DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON,
            "status_code": HTTPStatus.OK,
            "headers": HEADERS,
        }
    )
    mocker.patch(GENERIC_REST_CLIENT_V1_PATH, side_effect=async_mock)
    return async_mock


@pytest.mark.asyncio
@pytest.mark.document_types
class TestDocumentTypes:
    async def test_aggregate_document_types__deps_token_is_not_set__401(self, client, document_type_source_cache):
        res = await client.get(URL)

        assert res.status_code == 401

    @pytest.mark.usefixtures("mock_types_request")
    async def test_aggregate_document_types__successful(self, client, document_type_source_cache):
        res = await client.get(URL, headers=HEADERS)
        document_types = res.json()

        assert len(document_types) == len(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_JSON["result"]) + len(
            TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON
        )
        assert document_types[0].keys() == {"id", "code", "name", "language", "engine", "description", "createdAt"}
        assert all(p["code"] in document_type_source_cache for p in document_types)

    @pytest.mark.parametrize(
        "document_type_response, corleone_response",
        [
            (
                {
                    "content": copy.deepcopy(TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW),
                    "status_code": 200,
                    "headers": HEADERS,
                },
                Exception,
            ),
            (
                Exception,
                {
                    "content": copy.deepcopy(TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW),
                    "status_code": 200,
                    "headers": HEADERS,
                },
            ),
        ],
    )
    async def test_aggregate_document_types__one_of_services_unavailable__no_errors(
        self,
        client,
        mock_types_request,
        corleone_response,
        document_type_response,
    ):
        mock_types_request.side_effect = [corleone_response, document_type_response]
        res = await client.get(URL, headers=HEADERS)

        assert res.status_code == HTTPStatus.OK

    async def test_aggregate_document_types__services_unavailable__error(self, client):
        res = await client.get(URL, headers=HEADERS)

        assert res.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.skip("Fails on corleone data")
    @pytest.mark.usefixtures("mock_type_request")
    async def test_get_document_type__both_services_available__successful(self, client, document_type_source_cache):
        res = await client.get(f"{URL}/1", headers=HEADERS)

        assert res.status_code == HTTPStatus.OK

        document_type = res.json()

        assert document_type["id"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]
        assert document_type["code"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["id"]
        assert document_type["name"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["documentType"]
        assert document_type["language"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["language"]
        assert document_type["engine"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["engine"]
        assert document_type["fields"] == TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON["fields"]
        assert document_type["code"] in document_type_source_cache

    @pytest.mark.skip("Fails on corleone data")
    @pytest.mark.parametrize(
        "document_type_response, corleone_response",
        [
            (
                {
                    "content": TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
                    "status_code": 200,
                    "headers": HEADERS,
                },
                Exception,
            ),
            (
                Exception,
                {
                    "content": TYPE_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
                    "status_code": 200,
                    "headers": HEADERS,
                },
            ),
        ],
    )
    async def test_get_document_type__one_of_services_unavailable__success(
        self, client, mock_types_request, corleone_response, document_type_response
    ):
        mock_types_request.side_effect = [corleone_response, document_type_response]
        res = await client.get(f"{URL}/1", headers=HEADERS)

        assert res.status_code == HTTPStatus.OK

    async def test_put_document_type_llm__service_available__success(
        self,
        client,
        mock_type_response_from_type_service,
    ):
        res = await client.put(
            f"{BASE_API_V1_PREFIX}/document-types/1/llm",
            headers=HEADERS,
            data=UPDATE_DOCUMENT_TYPE_LLM_RAW_REQUEST,
        )

        assert res.status_code == HTTPStatus.OK

    async def test_put_document_type_llm__service_unavailable__error(
        self,
        client,
        mock_type_response_from_type_service,
    ):
        mock_type_response_from_type_service.side_effect = ClientError
        res = await client.put(
            f"{BASE_API_V1_PREFIX}/document-types/1/llm",
            headers=HEADERS,
            data=UPDATE_DOCUMENT_TYPE_LLM_RAW_REQUEST,
        )

        assert res.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.asyncio
    async def test_create_extraction_field__document_type_not_found(self, client, document_type_id):
        exception = {"code": "document_type_not_found", "message": "Document type with id: `type_id` not found"}
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields"
        with aioresponses() as mock_response:
            mock_response.post(extraction_url, status=HTTPStatus.NOT_FOUND, body=json.dumps(exception))

            response = await client.post(
                f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extraction-fields",
                data=json.dumps({"name": "name", "type": "string", "required": True}),
            )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == exception

    @pytest.mark.asyncio
    async def test_create_extraction_field___extractor_id_provided__created(self, client, document_type_id):
        raw_field = {"name": "name", "type": "string", "required": True, "extractorId": "testId"}
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields"
        with aioresponses() as mock_response:
            mock_response.post(extraction_url, status=HTTPStatus.CREATED, body=json.dumps(raw_field))

            response = await client.post(
                f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extraction-fields",
                data=json.dumps(raw_field),
            )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == raw_field

    @pytest.mark.asyncio
    async def test_create_extraction_field__service_unavailable(self, client, document_type_id):
        response = await client.post(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extraction-fields",
            data=json.dumps({"name": "name", "type": "string", "required": True}),
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert response.json()["code"] == "extraction_service_unavailable_error"

    @pytest.mark.asyncio
    async def test_get_document_types__success(self, client, mock_get_document_types_response_from_type_service):
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}/document-types"

        with aioresponses() as mock_response_extraction:
            mock_response_extraction.get(
                extraction_url, status=HTTPStatus.OK, body=DOCUMENT_TYPES_RESPONSE_FROM_EXTRACTION_SERVICE_JSON
            )

            response = await client.get(f"{BASE_API_V1_PREFIX}/document-types")

        assert response.status_code == HTTPStatus.OK

        document_types = response.json()

        assert document_types["result"]
        assert len(document_types["result"]) == 2

    @pytest.mark.asyncio
    async def test_get_document_types___services_unavailable(self, client):
        response = await client.get(f"{BASE_API_V1_PREFIX}/document-types")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["code"] == "document_type_error"

    @pytest.mark.asyncio
    async def test_get_document_type__success(
        self, client, mock_get_document_type_response_from_type_service, document_type_id
    ):
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V1_PREFIX}/document-types/{document_type_id}"

        with aioresponses() as mock_response_extraction:
            mock_response_extraction.get(
                extraction_url, status=HTTPStatus.OK, body=DOCUMENT_TYPE_RESPONSE_FROM_EXTRACTION_SERVICE_JSON
            )

            response = await client.get(f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}")

        assert response.status_code == HTTPStatus.OK

        document_type = response.json()

        assert len(document_type["fields"]) == 1

        expected_result = copy.deepcopy(DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT)

        expected_result["fields"] = DOCUMENT_TYPE_RESPONSE_FROM_EXTRACTION_SERVICE_DICT["fields"]

        assert response.json() == json.loads(
            DocumentTypeResponseData.from_response(expected_result).model_dump_json(by_alias=True)
        )

    @pytest.mark.asyncio
    async def test_get_document_type___services_unavailable(self, client, document_type_id):
        response = await client.get(f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["code"] == "document_type_error"

    @pytest.mark.asyncio
    async def test_update_extraction_field_with_prompt__updated(self, client, document_type_id, field_code):
        extraction_url = (
            f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields/{field_code}"
        )
        with aioresponses() as mock_response:
            mock_response.patch(
                extraction_url,
                status=HTTPStatus.OK,
                body=EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
            )

            response = await client.patch(
                f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extraction-fields/{field_code}",
                data=json.dumps(EXTRACTION_FIELD_WITH_PROMPT_REQUEST_DICT),
            )

        assert response.status_code == HTTPStatus.OK

        updated_field_with_prompt = response.json()

        assert updated_field_with_prompt == EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_DICT

    @pytest.mark.asyncio
    async def test_update_extraction_field_with_prompt__service_unavailable(self, client, document_type_id, field_code):
        response = await client.patch(
            f"{BASE_API_V1_PREFIX}/document-types/{document_type_id}/extraction-fields/{field_code}",
            data=json.dumps(EXTRACTION_FIELD_WITH_PROMPT_REQUEST_DICT),
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert response.json()["code"] == "extraction_service_unavailable_error"

    @pytest.mark.asyncio
    async def test_create_extraction_field__created(self, client, document_type_id):
        raw_field = {
            "name": "name",
            "code": "test_field_code",
            "type": "string",
            "required": True,
            "confidential": False,
            "readOnly": True,
            "order": 4,
            "description": {
                "char_type": "alphabetic",
                "char_whitelist": "whitelist",
                "char_blacklist": "blacklist",
                "display_char_limit": 10,
            },
        }
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields"
        with aioresponses() as mock_response:
            mock_response.post(extraction_url, status=HTTPStatus.CREATED, body=json.dumps(raw_field))

            response = await client.post(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extraction-fields",
                data=json.dumps(raw_field),
            )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == raw_field

    @pytest.mark.asyncio
    async def test_update_extraction_field__updated(
        self,
        client,
        document_type_id: str,
        field_code: str,
        extractor_id: str,
    ):
        extraction_url = (
            f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields/{field_code}"
            f"?extractorId={extractor_id}"
        )

        data = {
            "name": "name 2",
            "required": True,
            "confidential": False,
            "readOnly": True,
            "order": 4,
            "description": {
                "char_type": "alphabetic",
                "char_whitelist": "whitelist",
                "char_blacklist": "blacklist",
                "display_char_limit": 10,
            },
        }

        query_params = {"extractorId": extractor_id}

        with aioresponses() as mock_response:
            mock_response.patch(extraction_url, status=HTTPStatus.OK, body=UPDATE_EXTRACTION_FIELD_RESPONSE_JSON)

            response = await client.patch(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extraction-fields/{field_code}",
                json=data,
                params=query_params,
            )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == UPDATE_EXTRACTION_FIELD_RESPONSE_DICT

    @pytest.mark.asyncio
    async def test_delete_extraction_fields__deleted(self, client, document_type_id, field_code):
        params = {"fieldCodes": [field_code]}
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields?{urlencode(params, doseq=True)}"
        with aioresponses() as mock_response:
            mock_response.delete(extraction_url, status=HTTPStatus.NO_CONTENT)

            response = await client.delete(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extraction-fields",
                params=params,
            )

        assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.asyncio
    async def test_attach_extractor__created(self, client):
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/attach-extractor"
        with aioresponses() as mock_response:
            mock_response.post(
                extraction_url, status=HTTPStatus.CREATED, body=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE)
            )

            response = await client.post(
                f"{BASE_API_V5_PREFIX}/document-types/attach-extractor",
                data=json.dumps(DOCUMENT_TYPES_ATTACH_EXTRACTOR_REQUEST),
            )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == DOCUMENT_TYPES_ATTACH_EXTRACTOR_RESPONSE

    @pytest.mark.asyncio
    async def test_get_document_types_v5__ok(self, client):
        document_types_url = f"{DOCUMENT_TYPE_BASE_V2_URL}/types?extractionType=non"

        expected_response = copy.deepcopy(DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT)
        for doctype in expected_response["result"]:
            doctype["workflowConfiguration"] = None
        for doctype in expected_response["result"]:
            del doctype["fields"]

        with aioresponses() as mock_response:
            mock_response.get(document_types_url, body=DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON)

            data = {"extractionType": "non"}

            response = await client.get(f"{BASE_API_V5_PREFIX}/document-types", params=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_get_document_types_v5__with_workflow_configurations__ok(self, client):
        document_types_url = f"{DOCUMENT_TYPE_BASE_V2_URL}/types"
        workflow_configurations_url = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}/workflow-configuration"

        workflow_configurations_dict = copy.deepcopy(WORKFLOW_CONFIGURATIONS_RESPONSE_DICT)
        expected_response = copy.deepcopy(DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT)

        for doctype in expected_response["result"]:
            del doctype["fields"]
            doctype["workflowConfiguration"] = WORKFLOW_CONFIGURATION_RESPONSE_DICT
            workflow_configurations_dict[doctype["id"]] = WORKFLOW_CONFIGURATION_RESPONSE_DICT

        with aioresponses() as mock_response:
            mock_response.get(
                document_types_url,
                body=DOCUMENT_TYPES_RESPONSE_FROM_DOCUMENT_TYPE_WITH_WORKFLOW_CONFIGURATION_SERVICE_JSON,
            )
            mock_response.get(workflow_configurations_url, body=json.dumps(workflow_configurations_dict))
            data = {"workflowConfigurations": True}

            response = await client.get(f"{BASE_API_V5_PREFIX}/document-types", params=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == expected_response

    @pytest.mark.parametrize(
        "extras",
        (
            [DocumentTypeExtras.EXTRACTION_FIELDS.value],
            [DocumentTypeExtras.EXTRA_FIELDS.value],
            [DocumentTypeExtras.VALIDATORS.value],
            [DocumentTypeExtras.PROFILES.value],
            [DocumentTypeExtras.CLASSIFIERS.value],
            [DocumentTypeExtras.LLM_EXTRACTORS.value],
            [DocumentTypeExtras.WORKFLOW_CONFIGURATIONS.value],
            [
                DocumentTypeExtras.EXTRACTION_FIELDS.value,
                DocumentTypeExtras.EXTRA_FIELDS.value,
                DocumentTypeExtras.VALIDATORS.value,
                DocumentTypeExtras.PROFILES.value,
                DocumentTypeExtras.CLASSIFIERS.value,
                DocumentTypeExtras.LLM_EXTRACTORS.value,
                DocumentTypeExtras.WORKFLOW_CONFIGURATIONS.value,
            ],
            None,
        ),
    )
    @pytest.mark.asyncio
    async def test_get_document_type_v5__ok(
        self, client, document_type_id: str, extras: Optional[list[DocumentTypeExtras]]
    ):
        document_type_url = f"{DOCUMENT_TYPE_BASE_V1_URL}/types/{document_type_id}"
        extraction_url = f"{EXTRACTION_BASE_URL}/{document_type_id}"
        enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
        high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/{document_type_id}"
        output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/{document_type_id}/profiles"
        classification_url = f"{CLASSIFICATION_BASE_URL}/document-types/{document_type_id}/gen-ai-classifiers"
        ai_fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors"
        workflow_manager_url = f"{WORKFLOW_MANAGER_BASE_BASE_URL}/workflow-configuration/{document_type_id}"
        base_doctype = copy.deepcopy(DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT)
        base_doctype.update(
            {
                "extractionFields": None,
                "extraFields": None,
                "validators": None,
                "crossFieldValidators": None,
                "profiles": None,
                "classifiers": None,
                "llmExtractors": None,
                "workflowConfiguration": None,
            }
        )
        del base_doctype["fields"]

        with aioresponses() as mock_response:
            mock_response.get(document_type_url, body=DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON)
            mock_response.get(extraction_url, body=EXTRACTION_DOCUMENT_TYPE_RESPONSE__JSON)
            mock_response.get(enrichment_url, body=EXTRA_FIELDS_RESPONSE_JSON)
            mock_response.get(high_sparrow_url, body=HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_JSON)
            mock_response.get(output_exporting_url, body=OUTPUT_PROFILES_RESPONSE_JSON)
            mock_response.get(classification_url, body=GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_JSON)
            mock_response.get(ai_fusion_url, body=AI_FUSION_GET_LLM_EXTRACTORS_RESPONSE_JSON)
            mock_response.get(workflow_manager_url, body=WORKFLOW_CONFIGURATION_RESPONSE_JSON)

            data = {}
            if extras is not None:
                data["extras"] = extras

            response = await client.get(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}", params=data)

            assert response.status_code == HTTPStatus.OK

            if extras is not None:
                if DocumentTypeExtras.EXTRACTION_FIELDS in extras:
                    base_doctype["extractionFields"] = copy.deepcopy(
                        EXTRACTION_DOCUMENT_TYPE_RESPONSE_DICT["fields"]  # type: ignore
                    )
                if DocumentTypeExtras.EXTRA_FIELDS in extras:
                    base_doctype["extraFields"] = copy.deepcopy(EXTRA_FIELDS_RESPONSE_DICT["fields"])
                if DocumentTypeExtras.VALIDATORS in extras:
                    base_doctype["validators"] = copy.deepcopy(HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_DICT["validators"])
                    base_doctype["crossFieldValidators"] = copy.deepcopy(
                        HIGH_SPARROW_DOCUMENT_TYPE_RESPONSE_DICT["crossFieldValidators"],
                    )
                if DocumentTypeExtras.PROFILES in extras:
                    base_doctype["profiles"] = copy.deepcopy(OUTPUT_PROFILES_RESPONSE_DICT["profiles"])
                if DocumentTypeExtras.CLASSIFIERS in extras:
                    base_doctype["classifiers"] = copy.deepcopy(
                        GET_CLASSIFIERS_OF_DOCUMENT_TYPE_RESPONSE_DICT  # type: ignore
                    )
                if DocumentTypeExtras.LLM_EXTRACTORS in extras:
                    base_doctype["llmExtractors"] = copy.deepcopy(EXPECTED_LLM_EXTRACTORS_IN_DOCUMENT_TYPE_RESPONSE)
                if DocumentTypeExtras.WORKFLOW_CONFIGURATIONS in extras:
                    base_doctype["workflowConfiguration"] = copy.deepcopy(WORKFLOW_CONFIGURATION_RESPONSE_DICT)  # type: ignore
            assert response.json() == base_doctype

    @pytest.mark.asyncio
    async def test_get_document_type_v5__data_to_extras_not_found__empty_value(self, document_type_id: str, client):
        document_type_url = f"{DOCUMENT_TYPE_BASE_V1_URL}/types/{document_type_id}"
        extraction_url = f"{EXTRACTION_BASE_URL}/{document_type_id}"
        enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"
        high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/{document_type_id}"
        output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/{document_type_id}/profiles"
        classification_url = f"{CLASSIFICATION_BASE_URL}/document-types/{document_type_id}/gen-ai-classifiers"
        ai_fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors"
        workflow_manager_url = f"{WORKFLOW_MANAGER_BASE_BASE_URL}/workflow-configuration/{document_type_id}"

        expected_response = copy.deepcopy(DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_DICT)
        expected_response.update(
            {
                "extractionFields": None,
                "extraFields": None,
                "validators": None,
                "crossFieldValidators": None,
                "profiles": None,
                "classifiers": None,
                "llmExtractors": None,
                "workflowConfiguration": None,
            }
        )
        del expected_response["fields"]

        with aioresponses() as mock_response:
            mock_response.get(document_type_url, body=DOCUMENT_TYPE_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_JSON)
            mock_response.get(extraction_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            mock_response.get(enrichment_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            mock_response.get(high_sparrow_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            mock_response.get(output_exporting_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            mock_response.get(classification_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            mock_response.get(ai_fusion_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            mock_response.get(workflow_manager_url, body=b"{}", status=HTTPStatus.NOT_FOUND)
            data = {
                "extras": [
                    DocumentTypeExtras.EXTRACTION_FIELDS.value,
                    DocumentTypeExtras.EXTRA_FIELDS.value,
                    DocumentTypeExtras.VALIDATORS.value,
                    DocumentTypeExtras.PROFILES.value,
                    DocumentTypeExtras.CLASSIFIERS.value,
                    DocumentTypeExtras.LLM_EXTRACTORS.value,
                    DocumentTypeExtras.WORKFLOW_CONFIGURATIONS.value,
                ]
            }

            response = await client.get(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}", params=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == expected_response

    @pytest.mark.parametrize("src_template_id", [None, "string"])
    @pytest.mark.asyncio
    async def test_create_template__created(self, client, document_type_id: str, src_template_id: str):
        workflow_manager_url = f"{WORKFLOW_MANAGER_BASE_BASE_URL}/template-workflow"
        if src_template_id is not None:
            workflow_manager_url += "/from"

        data = {
            "name": "string",
            "language": "string",
            "engine": "string",
            "description": "string",
            "groupId": "string",
        }
        if src_template_id is not None:
            data["baseTemplateId"] = src_template_id

        with aioresponses() as mock_response:
            mock_response.post(workflow_manager_url, body=CREATE_TEMPLATE_RESPONSE_JSON, status=HTTPStatus.CREATED)

            response = await client.post(f"{BASE_API_V5_PREFIX}/document-types/template", json=data)

            assert response.status_code == HTTPStatus.CREATED
            assert response.json() == CREATE_TEMPLATE_RESPONSE_DICT

    @pytest.mark.asyncio
    async def test_create_template_version__with_empty_name(self, client, document_type_id: str):
        workflow_manager_url = f"{WORKFLOW_MANAGER_BASE_BASE_URL}/template-workflow/{document_type_id}/versions"

        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file1 = open(mock_file, "rb")
        with patch("builtins.open", mock_open(read_data="file2")) as mock_file:
            file2 = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("name", ""),
                ("description", "string"),
                ("markupAutomatically", str(True)),
            ]
        )
        files = [
            ("files", (uuid.uuid4().hex, file1)),
            ("files", (uuid.uuid4().hex, file2)),
        ]
        with aioresponses() as mock_response:
            mock_response.post(workflow_manager_url, status=HTTPStatus.CREATED)

            response = await client.post(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions", files=files, data=data
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_template_version__created(self, client, document_type_id: str):
        workflow_manager_url = f"{WORKFLOW_MANAGER_BASE_BASE_URL}/template-workflow/{document_type_id}/versions"

        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file1 = open(mock_file, "rb")
        with patch("builtins.open", mock_open(read_data="file2")) as mock_file:
            file2 = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("name", "string"),
                ("description", "string"),
                ("markupAutomatically", str(True)),
            ]
        )
        files = [
            ("files", (uuid.uuid4().hex, file1)),
            ("files", (uuid.uuid4().hex, file2)),
        ]
        with aioresponses() as mock_response:
            mock_response.post(workflow_manager_url, status=HTTPStatus.CREATED)

            response = await client.post(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions", files=files, data=data
            )

            assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.asyncio
    async def test_get_template_versions__ok(self, client, document_type_id: str):
        template_url = f"{TEMPLATE_BASE_BASE_URL}/{document_type_id}/versions"

        with aioresponses() as mock_response:
            mock_response.get(template_url, body=GET_TEMPLATE_VERSIONS_RESPONSE_JSON)

            response = await client.get(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions")

            assert response.status_code == HTTPStatus.OK
            assert response.json() == GET_TEMPLATE_VERSIONS_RESPONSE_DICT

    @pytest.mark.asyncio
    async def test_get_template_version__ok(self, client, document_type_id: str, template_version_id: str):
        template_url = f"{TEMPLATE_BASE_BASE_URL}/{document_type_id}/versions/{template_version_id}"

        with aioresponses() as mock_response:
            mock_response.get(template_url, body=SERIALIZED_TEMPLATE_VERSION_RESPONSE_JSON)

            response = await client.get(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions/{template_version_id}"
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == SERIALIZED_TEMPLATE_VERSION_RESPONSE_DICT

    @pytest.mark.asyncio
    async def test_raname_template_version__ok(self, client, document_type_id: str, template_version_id: str):
        template_url = f"{TEMPLATE_BASE_BASE_URL}/{document_type_id}/versions/{template_version_id}/name"

        data = {"name": "string"}

        with aioresponses() as mock_response:
            mock_response.patch(template_url, body=SERIALIZED_TEMPLATE_VERSION_RESPONSE_JSON)

            response = await client.patch(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions/{template_version_id}",
                json=data,
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == SERIALIZED_TEMPLATE_VERSION_RESPONSE_DICT

    @pytest.mark.asyncio
    async def test_delete_template_versions__no_content(self, client, document_type_id: str):
        template_url = f"{TEMPLATE_BASE_BASE_URL}/{document_type_id}/versions"

        data = {"ids": ["string1", "string2"]}

        with aioresponses() as mock_response:
            mock_response.delete(template_url, status=HTTPStatus.NO_CONTENT)

            response = await client.delete(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions",
                params=data,
            )

            assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.asyncio
    async def test_add_markup__ok(self, client, document_type_id: str, template_version_id: str):
        template_url = f"{TEMPLATE_BASE_BASE_URL}/{document_type_id}/versions/{template_version_id}/markups"

        data = {
            "referencePage": "string",
            "markups": {"string": [[1, 2, 3, 4]]},
            "markupTypes": {"string": "string"},
        }

        with aioresponses() as mock_response:
            mock_response.put(template_url, status=HTTPStatus.OK)

            response = await client.put(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/template/versions/{template_version_id}/markups",
                json=data,
            )

            assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_delete_document_type__no_content(self, client, document_type_id: str):
        document_type_url = f"{DOCUMENT_TYPE_BASE_V1_URL}/types/{document_type_id}"

        with aioresponses() as mock_response:
            mock_response.delete(document_type_url, status=HTTPStatus.NO_CONTENT)

            response = await client.delete(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}")

            assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.asyncio
    async def test_save_extra_fields__ok(self, client: AsyncClient, document_type_id: str):
        enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"

        data = {"name": "test", "order": 123}

        with aioresponses() as mock_response:
            mock_response.post(enrichment_url, status=HTTPStatus.CREATED)

            response = await client.post(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extra-fields",
                json=data,
            )

            assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.asyncio
    async def test_update_extra_fields__ok(self, client: AsyncClient, document_type_id: str):
        enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields"

        data = {
            "extraFields": [
                {"code": "test1", "name": "testname1", "order": 1},
                {"code": "test2", "name": "testname2", "order": 2},
            ]
        }

        with aioresponses() as mock_response:
            mock_response.put(enrichment_url, status=HTTPStatus.CREATED)

            response = await client.put(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extra-fields",
                json=data,
            )

            assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.asyncio
    async def test_delete_extra_fields__ok(self, client: AsyncClient, document_type_id: str):
        enrichment_url = f"{ENRICHMENT_BASE_URL}/{document_type_id}/extra-fields?extraFieldCodes=1&extraFieldCodes=2"

        data = {"extraFieldCodes": ["1", "2"]}

        with aioresponses() as mock_response:
            mock_response.delete(enrichment_url, status=HTTPStatus.NO_CONTENT)

            response = await client.delete(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extra-fields",
                params=data,
            )

            assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.asyncio
    async def test_save_profiles__ok(self, client: AsyncClient, document_type_id: str):
        output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/{document_type_id}/profiles"

        data = {
            "name": "test",
            "schema": {
                "fields": ["test"],
                "needsValidationResults": False,
            },
            "format": "json",
            "externalStoragesInfo": [
                {
                    "code": "Salesforce",
                    "credentials": {
                        "clientId": "test",
                        "clientSecret": "test",
                        "ownerId": "test",
                        "locationId": "test",
                    },
                    "outputDirectoryPath": "test",
                },
            ],
        }

        with aioresponses() as mock_response:
            mock_response.post(output_exporting_url, status=HTTPStatus.CREATED)

            response = await client.post(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/profiles",
                json=data,
            )

            assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.asyncio
    async def test_update_profiles__ok(self, client: AsyncClient, document_type_id: str):
        output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/{document_type_id}/profiles/test"

        data = {
            "name": "test",
            "schema": {
                "fields": ["test"],
                "needsValidationResults": False,
            },
        }

        with aioresponses() as mock_response:
            mock_response.put(output_exporting_url, status=HTTPStatus.OK)

            response = await client.put(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/profiles/test",
                json=data,
            )

            assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_delete_profile__ok(self, client: AsyncClient, document_type_id: str):
        output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/{document_type_id}/profiles/test"

        with aioresponses() as mock_response:
            mock_response.delete(output_exporting_url, status=HTTPStatus.NO_CONTENT)

            response = await client.delete(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/profiles/test")

            assert response.status_code == HTTPStatus.NO_CONTENT

    @pytest.mark.asyncio
    async def test_update_llm__ok(self, client: AsyncClient, document_type_id: str):
        document_type_url = f"{DOCUMENT_TYPE_BASE_V1_URL}/types/{document_type_id}/llm"

        data = {"llmType": "test"}

        with aioresponses() as mock_response:
            mock_response.put(document_type_url, status=HTTPStatus.OK)

            response = await client.put(f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/llm", json=data)

            assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_update_fields__updated(self, client, document_type_id, field_code):
        extraction_url = f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extraction-fields"
        with aioresponses() as mock_response:
            mock_response.patch(
                extraction_url,
                status=HTTPStatus.OK,
                body=EXTRACTION_FIELDS_RESPONSE_FROM_EXTRACTION_SERVICE_JSON,
            )

            response = await client.patch(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extraction-fields",
                data=json.dumps({"fields": [{"code": field_code, **EXTRACTION_FIELD_WITH_PROMPT_REQUEST_DICT}]}),
            )

        assert response.status_code == HTTPStatus.OK

        updated_field_with_prompt = response.json()

        assert updated_field_with_prompt == {
            "fields": [EXTRACTION_FIELD_WITH_PROMPT_RESPONSE_FROM_EXTRACTION_SERVICE_JSON]
        }

    @pytest.mark.asyncio
    async def test_update_fields__service_unavailable(self, client, document_type_id, field_code):
        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extraction-fields",
            data=json.dumps({"fields": [{"code": field_code, **EXTRACTION_FIELD_WITH_PROMPT_REQUEST_DICT}]}),
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        assert response.json()["code"] == "extraction_service_unavailable_error"

    @pytest.mark.asyncio
    async def test_detach_extractor__no_content(self, client, document_type_id: str, extractor_id: str):
        extraction_url = (
            f"{EXTRACTION_BASE_API_PREFIX}{V2_PREFIX}/document-types/{document_type_id}/extractors/{extractor_id}"
        )

        with aioresponses() as mocked:
            mocked.delete(extraction_url, status=HTTPStatus.NO_CONTENT)

            response = await client.delete(
                f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/extractors/{extractor_id}",
            )

        assert response.status_code == HTTPStatus.NO_CONTENT
