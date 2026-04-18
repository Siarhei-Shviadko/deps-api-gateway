import copy
import json
import urllib.parse
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Mapping, Optional
from unittest.mock import mock_open, patch

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient
from multidict import CIMultiDict

from deps_api_gateway.application import DocumentDetailExtras
from deps_api_gateway.application.legacy.document.cacher import RareCacheKeys
from deps_api_gateway.application.legacy.document.document import _Endpoints
from deps_api_gateway.constants import (
    AI_FUSION_BASE_PREFIX,
    API_PREFIX,
    BASE_API_V5_PREFIX,
    BASE_API_V6_PREFIX,
    DOCUMENT_BASE_API_PREFIX,
    HIGH_SPARROW_BASE_PREFIX,
    OUTPUT_EXPORTING_BASE_PREFIX,
    PARSING_BASE_API_PREFIX,
    V1_PREFIX,
    V2_PREFIX,
    WORKFLOW_MANAGER_BASE_API_PREFIX,
    DocumentTypeSource,
)
from tests.data.ai_fusion_json_data import (
    AI_FUSION_CONVERSATION_GET_RESPONSE_DATA_DICT,
    AI_FUSION_CONVERSATION_GET_RESPONSE_JSON,
)
from tests.data.document_json_data import (
    ADD_COMMENT_RESPONSE_DICT,
    ADD_COMMENT_RESPONSE_JSON,
    ADD_LABEL_ON_DOCUMENT_RESPONSE_DICT,
    ADD_LABEL_ON_DOCUMENT_RESPONSE_JSON,
    CREATE_LABEL_RESPONSE_DICT,
    CREATE_LABEL_RESPONSE_JSON,
    DELETE_DOCUMENT_LIST_RESPONSE_JSON,
    DOCUMENT_DETAIL_RESPONSE_DICT,
    DOCUMENT_DETAIL_RESPONSE_JSON,
    DOCUMENT_LIST_NO_META_RESPONSE_DICT,
    DOCUMENT_LIST_RESPONSE_DICT,
    DOCUMENT_LIST_RESPONSE_JSON,
    DOCUMENT_METADATA_RESPONSE_DICT,
    DOCUMENT_METADATA_RESPONSE_JSON,
    GET_LABELS_RESPONSE_DICT,
    GET_LABELS_RESPONSE_JSON,
    GET_STATES_RESPONSE_DICT,
    GET_STATES_RESPONSE_JSON,
    PARTIAL_UPDATE_DOCUMENT_RESPONSE_DICT,
    PARTIAL_UPDATE_DOCUMENT_RESPONSE_JSON,
    REMOVE_LABEL_FROM_DOCUMENT_JSON,
)
from tests.data.json_data import (
    DOCUMENT_STATES_RESPONSE,
    OCR_ENGINES_RESPONSE,
    OCR_LANGUAGES_RESPONSE,
    RAW_DOCUMENT_STATES_RESPONSE,
    RAW_OCR_ENGINES_RESPONSE,
    RAW_OCR_LANGUAGES_RESPONSE,
    RESPONSE_FROM_DOCUMENT_SERVICE_RAW,
    TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW,
    TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW,
)
from tests.data.output_exporting_json_data import OUTPUTS_DICT, OUTPUTS_JSON
from tests.data.parsing_json_data import PARSING_INFO_DICT, PARSING_INFO_JSON
from tests.data.validation_json_data import (
    HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT,
    HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON,
)

HEADERS = {"deps-token": '{"organisation": "deps-users"}'}
URL = f"{API_PREFIX}/documents"
GENERIC_REST_CLIENT_PATH = "deps_api_gateway.infrastructure.proxies.document.proxy.DocumentProxy.request"
DOCUMENT_SERVICE_BASE_V1_URL = f"{DOCUMENT_BASE_API_PREFIX}{V1_PREFIX}"
DOCUMENT_SERVICE_BASE_V2_URL = f"{DOCUMENT_BASE_API_PREFIX}{V2_PREFIX}"
HIGH_SPARROW_BASE_URL = f"{HIGH_SPARROW_BASE_PREFIX}{V1_PREFIX}"
OUTPUT_EXPORTING_BASE_URL = f"{OUTPUT_EXPORTING_BASE_PREFIX}{V1_PREFIX}"
AI_FUSION_BASE_URL = f"{AI_FUSION_BASE_PREFIX}{V1_PREFIX}"
WORKFLOW_MANAGER_V1_URL = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V1_PREFIX}"
WORKFLOW_MANAGER_V2_URL = f"{WORKFLOW_MANAGER_BASE_API_PREFIX}{V2_PREFIX}"
PARSING_INFO_BASE_URL = f"{PARSING_BASE_API_PREFIX}{V2_PREFIX}"


@pytest.fixture
def successful_full_response():
    return {
        "result": [
            {
                "date": "2023-01-27",
                "documentType": {"code": "1", "name": "new_type_2"},
                "engine": {"code": "TESSERACT", "name": "Tesseract"},
                "id": "82",
                "labels": [],
                "language": {"code": "eng", "name": "English"},
                "reviewer": None,
                "state": {"code": "dataExtraction", "name": "Data Extraction"},
                "title": "4506-C searchable-1",
            }
        ],
        "size": 1,
        "total": 3,
    }


@pytest.fixture
def successful_corleone_only_response(successful_full_response):
    successful_full_response["result"][0]["documentType"] = None
    return successful_full_response


@pytest.fixture(scope="module")
def endpoints():
    yield _Endpoints()


@pytest.fixture
def shared_response_mocks(endpoints):
    with aioresponses() as response:
        response.get(endpoints.document_list, body=RESPONSE_FROM_DOCUMENT_SERVICE_RAW)
        response.get(endpoints.ocr_engines, body=RAW_OCR_ENGINES_RESPONSE)
        response.get(endpoints.ocr_languages, body=RAW_OCR_LANGUAGES_RESPONSE)
        response.get(endpoints.document_states, body=RAW_DOCUMENT_STATES_RESPONSE)
        yield response
    response.clear()


@pytest.fixture
def successful_corleone_response(shared_response_mocks, endpoints):
    response = shared_response_mocks
    response.get(endpoints.corleone_types, body=TYPES_RESPONSE_FROM_CORLEONE_SERVICE_RAW)
    yield response


@pytest.fixture
def successful_doc_type_response(shared_response_mocks, endpoints):
    response = shared_response_mocks
    response.get(endpoints.document_type_types, body=TYPES_RESPONSE_FROM_DOCUMENT_TYPE_SERVICE_RAW)
    return response


@pytest.fixture
def failed_corleone_response(shared_response_mocks, endpoints):
    response = shared_response_mocks
    response.get(endpoints.corleone_types, status=404)
    yield response


@pytest.fixture
def failed_doc_type_response(shared_response_mocks, endpoints):
    response = shared_response_mocks
    response.get(endpoints.document_type_types, status=404)
    yield response


@pytest.mark.asyncio
@pytest.mark.documents
class TestDocuments:
    async def test_get_document_list__ok(self, client: AsyncClient):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents"
        start_date = datetime(2025, 1, 15, tzinfo=timezone.utc).isoformat()
        end_date = datetime(2025, 4, 16, tzinfo=timezone.utc).isoformat()

        data = {
            "states": ["new", "preprocessing"],
            "types": ["string"],
            "title": "string",
            "exceptTypes": ["string", "string"],
            "reviewer": "string",
            "engines": ["TESSERACT"],
            "sortField": "title",
            "sortDirect": "asc",
            "page": 1,
            "perPage": 10,
            "labels": ["string"],
            "hasReviewer": True,
            "search": "string",
            "filterIds": [123],
            "dateRange": [start_date, end_date],
        }
        query_data = {
            key: json.dumps(value) if isinstance(value, (list, bool)) else value for key, value in data.items()
        }

        with aioresponses() as mock_response:
            mock_response.get(
                f"{document_service_url}?{urllib.parse.urlencode(query_data, doseq=True)}",
                body=DOCUMENT_LIST_RESPONSE_JSON,
            )

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents", params=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == DOCUMENT_LIST_RESPONSE_DICT

    @pytest.mark.parametrize(
        "extras",
        (
            [DocumentDetailExtras.OUTPUTS.value],
            [DocumentDetailExtras.CONVERSATION.value],
            [DocumentDetailExtras.VALIDATION_RESULTS.value],
            [DocumentDetailExtras.METADATA.value],
            [DocumentDetailExtras.PARSING_INFO.value],
            [
                DocumentDetailExtras.OUTPUTS.value,
                DocumentDetailExtras.CONVERSATION.value,
                DocumentDetailExtras.VALIDATION_RESULTS.value,
                DocumentDetailExtras.METADATA.value,
                DocumentDetailExtras.PARSING_INFO.value,
            ],
            None,
        ),
    )
    async def test_get_document_detail(self, client, document_id: str, extras: Optional[list[DocumentDetailExtras]]):
        document_detail_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/{document_id}"
        output_exporting_url = f"{OUTPUT_EXPORTING_BASE_URL}/document/{document_id}/outputs"
        ai_fusion_url = f"{AI_FUSION_BASE_URL}/conversations/{document_id}"
        high_sparrow_url = f"{HIGH_SPARROW_BASE_URL}/results/{document_id}"
        document_metadata_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/{document_id}/metadata"
        parsing_info_url = f"{PARSING_INFO_BASE_URL}/documents/{document_id}/parsing-info"

        data = {}
        if extras is not None:
            data["extras"] = extras

        base_document_detail = copy.deepcopy(DOCUMENT_DETAIL_RESPONSE_DICT)
        base_document_detail.update(
            {
                "outputs": None,
                "conversation": None,
                "validationResults": None,
                "metadata": None,
                "parsingInfo": None,
            }
        )

        with aioresponses() as mock_response:
            mock_response.get(document_detail_url, body=DOCUMENT_DETAIL_RESPONSE_JSON)
            mock_response.get(output_exporting_url, body=OUTPUTS_JSON)
            mock_response.get(ai_fusion_url, body=AI_FUSION_CONVERSATION_GET_RESPONSE_JSON)
            mock_response.get(high_sparrow_url, body=HIGH_SPARROW_VALIDATION_RESULTS_VALID_JSON)
            mock_response.get(document_metadata_url, body=DOCUMENT_METADATA_RESPONSE_JSON)
            mock_response.get(parsing_info_url, body=PARSING_INFO_JSON)

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}", params=data)

            assert response.status_code == HTTPStatus.OK

            if extras is not None:
                if DocumentDetailExtras.OUTPUTS in extras:
                    base_document_detail["outputs"] = OUTPUTS_DICT["outputs"]
                if DocumentDetailExtras.CONVERSATION in extras:
                    base_document_detail["conversation"] = AI_FUSION_CONVERSATION_GET_RESPONSE_DATA_DICT
                if DocumentDetailExtras.VALIDATION_RESULTS in extras:
                    base_document_detail["validationResults"] = HIGH_SPARROW_VALIDATION_RESULTS_VALID_DICT
                if DocumentDetailExtras.METADATA in extras:
                    base_document_detail["metadata"] = DOCUMENT_METADATA_RESPONSE_DICT["metadata"]
                if DocumentDetailExtras.PARSING_INFO in extras:
                    base_document_detail["parsingInfo"] = PARSING_INFO_DICT

            assert response.json() == base_document_detail

    async def test_partial_update_document__ok(self, client, document_id):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/{document_id}"
        data = {
            "title": "string",
            "state": "new",
            "files": [{"blobName": "string"}],
            "documentType": "string",
            "modelName": "string",
            "date": "string",
            "source": "string",
            "reviewer": {"id": "string", "email": "string", "firstName": "string", "lastName": "string"},
            "language": "string",
            "engine": "string",
            "previewDocuments": {
                "1": {"blobName": "string"},
            },
            "processingDocuments": {
                "1": {"blobName": "string"},
            },
            "error": {"description": "", "inState": "new"},
            "containerType": "email",
            "containerMetadata": {
                "firstLevelChildCount": 1,
                "subject": "string",
                "sender": "string",
                "recipients": ["string"],
                "cc": ["string"],
                "body": "string",
                "date": "string",
            },
        }

        with aioresponses() as mock_response:
            mock_response.patch(document_service_url, body=PARTIAL_UPDATE_DOCUMENT_RESPONSE_JSON)

            response = await client.patch(f"{BASE_API_V5_PREFIX}/documents/{document_id}", json=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == PARTIAL_UPDATE_DOCUMENT_RESPONSE_DICT

    async def test_delete_document_list__no_content(self, client):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents"

        data = {"documentIds": ["1", "2"]}

        with aioresponses() as mock_response:
            mock_response.delete(document_service_url, body=DELETE_DOCUMENT_LIST_RESPONSE_JSON)

            response = await client.delete(f"{BASE_API_V5_PREFIX}/documents", params=data)

            assert response.status_code == HTTPStatus.NO_CONTENT
            assert not response.content

    @pytest.mark.parametrize(
        "document_ids",
        [
            "documentIds=0",
            "documentIds=-1",
            "documentIds=-1&documentIds=-2",
            "documentIds=-1&documentIds=1",
            "documentIds=someNotExistingDocumentId",
            "documentIds=9999999999",
            "documentIds=",
        ],
    )
    async def test_delete_document_list__invalid_params(self, client, document_ids):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents"

        with aioresponses() as mock_response:
            mock_response.delete(document_service_url, body=DELETE_DOCUMENT_LIST_RESPONSE_JSON)

            response = await client.delete(f"{BASE_API_V5_PREFIX}/documents?{document_ids}")

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_add_comment__ok(self, client, document_id):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/add-comment"

        data = {"text": "string"}

        with aioresponses() as mock_response:
            mock_response.post(document_service_url, body=ADD_COMMENT_RESPONSE_JSON)

            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/{document_id}/comments", json=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == ADD_COMMENT_RESPONSE_DICT

    async def test_get_labels__ok(self, client):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/labels"
        with aioresponses() as mock_response:
            mock_response.get(document_service_url, body=GET_LABELS_RESPONSE_JSON)

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents/labels")

            assert response.status_code == HTTPStatus.OK
            assert response.json() == GET_LABELS_RESPONSE_DICT

    async def test_remove_label_from_document__no_content(self, client, document_id, label_id):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/remove-label"
        with aioresponses() as mock_response:
            mock_response.post(document_service_url, body=REMOVE_LABEL_FROM_DOCUMENT_JSON)

            response = await client.delete(f"{BASE_API_V5_PREFIX}/documents/{document_id}/labels/{label_id}")

            assert response.status_code == HTTPStatus.NO_CONTENT
            assert not response.content

    async def test_create_label__ok(self, client):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/labels"
        data = {"labelName": "string"}

        with aioresponses() as mock_response:
            mock_response.post(document_service_url, body=CREATE_LABEL_RESPONSE_JSON)

            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/labels", json=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == CREATE_LABEL_RESPONSE_DICT

    async def test_add_label_on_document__ok(self, client, document_id, label_id):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/add-label"
        data = {"labelId": label_id}

        with aioresponses() as mock_response:
            mock_response.post(document_service_url, body=ADD_LABEL_ON_DOCUMENT_RESPONSE_JSON)

            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/{document_id}/labels", json=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == ADD_LABEL_ON_DOCUMENT_RESPONSE_DICT

    async def test_add_label_on_documents_batch__ok(self, client: AsyncClient, document_id: str, label_id: str):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/add-label"
        params = {"documentIds": [document_id]}
        data = {"labelId": label_id}

        with aioresponses() as mock_response:
            mock_response.post(url=document_service_url, body=json.dumps(DOCUMENT_LIST_NO_META_RESPONSE_DICT["result"]))
            response = await client.post(
                f"{BASE_API_V5_PREFIX}/documents/attach-labels",
                json=data,
                params=params,
            )

            assert response.status_code == HTTPStatus.OK
            assert response.json() == DOCUMENT_LIST_NO_META_RESPONSE_DICT

    async def test_get_states__ok(self, client):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/states"

        expected_result = {
            "states": [{"name": state["name"], "title": state["title"]} for state in GET_STATES_RESPONSE_DICT.values()]
        }

        with aioresponses() as mock_response:
            mock_response.get(document_service_url, body=GET_STATES_RESPONSE_JSON)

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents/states")

            assert response.status_code == HTTPStatus.OK
            assert response.json() == expected_result

    async def test_get_document_metadata__ok(self, client, document_id: str):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/{document_id}/metadata"

        with aioresponses() as mock_response:
            mock_response.get(document_service_url, body=DOCUMENT_METADATA_RESPONSE_JSON)

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/metadata")

            assert response.status_code == HTTPStatus.OK
            assert response.json() == DOCUMENT_METADATA_RESPONSE_DICT

    async def test_download_original_files__ok(self, client, document_id: str):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/{document_id}/files"

        with aioresponses() as mock_response:
            mock_response.get(document_service_url, body=b"file")

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/files")

            assert response.status_code == HTTPStatus.OK
            assert response.content == b"file"

    async def test_download_preprocessed_files__ok(self, client, document_id: str):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/{document_id}/preprocessed-images"

        with aioresponses() as mock_response:
            mock_response.get(document_service_url, body=b"file")

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents/{document_id}/preprocessed-files")

            assert response.status_code == HTTPStatus.OK
            assert response.content == b"file"

    async def test_upload_document__ok(self, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V2_URL}/upload-document"

        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file_ = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("documentName", "test"),
                ("documentType", "test"),
                ("parsingFeatures", '["images", "text"]'),
            ]
        )
        files = {"file": (uuid.uuid4().hex, file_)}

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.CREATED)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/upload", files=files, data=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.parametrize(
        "workflow_params",
        [
            (
                ("needsExtraction", True),
                ("needsParsing", True),
                ("needsValidation", True),
                ("needsReview", "always_review"),
                ("needsOutputExporting", True),
            ),
            tuple(),
        ],
    )
    @pytest.mark.current_test
    async def test_create_document__ok(self, workflow_params: tuple, client: AsyncClient) -> None:
        document_url = f"{DOCUMENT_SERVICE_BASE_V2_URL}/documents"

        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file_ = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("documentName", "test"),
                ("documentType", "test"),
                ("parsingFeatures", '["images", "text"]'),
                ("metadata", '{"test": "test"}'),
                ("engine", uuid.uuid4().hex),
                ("language", uuid.uuid4().hex),
                ("groupId", uuid.uuid4().hex),
                ("llmType", uuid.uuid4().hex),
                ("needsUnifier", "True"),
                ("assignedToMe", "True"),
                *workflow_params,
            ]
        )
        files = {"file": (uuid.uuid4().hex, file_)}
        with aioresponses() as mock_response:
            mock_response.post(url=document_url, status=HTTPStatus.CREATED)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents", files=files, data=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.CREATED

    async def test_create_document_with_labes__ok(self, client: AsyncClient) -> None:
        document_url = f"{DOCUMENT_SERVICE_BASE_V2_URL}/documents"

        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file_ = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("documentName", "test"),
                ("documentType", "test"),
                ("parsingFeatures", '["images", "text"]'),
                ("metadata", '{"test": "test"}'),
                ("engine", uuid.uuid4().hex),
                ("language", uuid.uuid4().hex),
                ("groupId", uuid.uuid4().hex),
                ("llmType", uuid.uuid4().hex),
                ("needsUnifier", "True"),
                ("needsExtraction", "True"),
                ("needsParsing", "True"),
                ("assignedToMe", "True"),
                ("labelIds", "[1, 2, 3]"),
            ]
        )
        files = {"file": (uuid.uuid4().hex, file_)}

        with aioresponses() as mock_response:
            mock_response.post(url=document_url, status=HTTPStatus.CREATED)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents", files=files, data=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.parametrize(
        "workflow_params",
        [
            {
                "invokeParsing": True,
                "invokeValidation": True,
                "needsReview": "always_review",
                "invokeOutputExporting": True,
            },
            {},
        ],
    )
    @pytest.mark.current_test
    async def test_import_document__ok(self, workflow_params: dict, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V2_URL}/import-documents"

        data = {
            "paths": ["path1", "path2"],
            "source": "GoogleDrive",
            "documentType": "test",
            "parsingFeatures": ["images", "text"],
            **workflow_params,
        }

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.OK)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/import", json=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize(
        "workflow_params",
        [
            (
                ("needsExtraction", True),
                ("needsParsing", True),
                ("needsValidation", True),
                ("needsReview", "always_review"),
                ("needsOutputExporting", True),
            ),
            tuple(),
        ],
    )
    async def test_create_document_v6__ok(self, workflow_params: tuple, client: AsyncClient) -> None:
        document_url = f"{DOCUMENT_SERVICE_BASE_V2_URL}/documents"

        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file_ = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("documentName", "test"),
                ("documentType", "test"),
                ("parsingFeatures", '["images", "text"]'),
                ("metadata", '{"test": "test"}'),
                ("engine", uuid.uuid4().hex),
                ("language", uuid.uuid4().hex),
                ("groupId", uuid.uuid4().hex),
                ("llmType", uuid.uuid4().hex),
                ("needsUnifier", "True"),
                ("assignedToMe", "True"),
                *workflow_params,
            ]
        )
        files = {"file": (uuid.uuid4().hex, file_)}

        with aioresponses() as mock_response:
            mock_response.post(url=document_url, status=HTTPStatus.CREATED)
            response = await client.post(f"{BASE_API_V6_PREFIX}/documents", files=files, data=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.CREATED

    async def test_create_document_v6__missing_document_type__422(self, client: AsyncClient) -> None:
        with patch("builtins.open", mock_open(read_data="file1")) as mock_file:
            file_ = open(mock_file, "rb")

        data: Mapping = CIMultiDict(
            [
                ("documentName", "test"),
                ("parsingFeatures", "[]"),
            ]
        )
        files = {"file": (uuid.uuid4().hex, file_)}

        response = await client.post(f"{BASE_API_V6_PREFIX}/documents", files=files, data=data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "workflow_params",
        [
            {
                "invokeParsing": True,
                "invokeValidation": True,
                "invokeReview": "always_review",
                "invokeOutputExporting": True,
            },
            {},
        ],
    )
    async def test_import_document_v6__ok(self, workflow_params: dict, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V2_URL}/import-documents"

        data = {
            "paths": ["path1", "path2"],
            "source": "GoogleDrive",
            "documentType": "test",
            "parsingFeatures": ["images", "text"],
            **workflow_params,
        }

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.OK)
            response = await client.post(f"{BASE_API_V6_PREFIX}/documents/import", json=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    async def test_import_document_v6__missing_document_type__422(self, client: AsyncClient) -> None:
        data = {
            "paths": ["path1", "path2"],
            "source": "GoogleDrive",
            "parsingFeatures": ["images", "text"],
        }

        response = await client.post(f"{BASE_API_V6_PREFIX}/documents/import", json=data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_validate_document__ok(self, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V1_URL}/validate-workflow"

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.OK)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/123/validate")

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    async def test_retry_last_failed_step__ok(self, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V2_URL}/retry-pipeline-last-step"

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.ACCEPTED)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/123/pipelines/retry")

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.ACCEPTED

    async def test_run_from_first_step__ok(self, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V2_URL}/run-pipeline"

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.ACCEPTED)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/123/pipelines/reprocess")

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.ACCEPTED

    async def test_run_from_step__ok(self, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V2_URL}/run-pipeline-from-step"

        data = {
            "documentIds": ["123", "124"],
            "step": "new",
            "parsingFeatures": ["images", "text"],
        }

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.ACCEPTED)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/pipelines/from-step", json=data)

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.ACCEPTED

    async def test_start_review__ok(self, client: AsyncClient) -> None:
        documents_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/start-review"

        with aioresponses() as mock_response:
            mock_response.post(url=documents_url, status=HTTPStatus.OK)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/123/review/start")

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    async def test_complete_review__ok(self, client: AsyncClient) -> None:
        workflow_manager_url = f"{WORKFLOW_MANAGER_V1_URL}/complete-review-workflow"

        with aioresponses() as mock_response:
            mock_response.post(url=workflow_manager_url, status=HTTPStatus.OK)
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/123/review/complete")

            mock_response.assert_called_once()
            assert response.status_code == HTTPStatus.OK

    async def test_assign_type__ok(self, client: AsyncClient, document_id: str, document_type_id: str) -> None:
        document_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/assign-type"
        data = {"documentTypeId": document_type_id}

        with aioresponses() as mock_response:
            mock_response.post(url=document_url, status=HTTPStatus.OK, body=json.dumps([DOCUMENT_DETAIL_RESPONSE_DICT]))
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/{document_id}/assign-type", json=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == DOCUMENT_DETAIL_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.document_list
class TestDocumentList:
    async def test_documents__deps_token_is_not_set__401(self, client):
        res = await client.get(URL)

        assert res.status_code == 401

    @pytest.mark.usefixtures("successful_corleone_response", "successful_doc_type_response")
    async def test_documents__valid_responses__successful(self, client, successful_full_response):
        res = await client.get(URL, headers=HEADERS)
        documents = res.json()
        assert documents == successful_full_response

    @pytest.mark.usefixtures("failed_corleone_response", "failed_doc_type_response")
    async def test_documents__no_data_from_doctypes_and_corleone__raises(self, client):
        res = await client.get(URL, headers=HEADERS)
        assert res.status_code == 400
        assert res.json()["message"] == "Can't get document types!"

    @pytest.mark.usefixtures("successful_corleone_response", "failed_doc_type_response")
    async def test_documents__no_data_from_doctypes__successful(self, client, successful_corleone_only_response):
        res = await client.get(URL, headers=HEADERS)
        documents = res.json()
        assert documents == successful_corleone_only_response

    @pytest.mark.usefixtures("failed_corleone_response", "successful_doc_type_response")
    async def test_documents__no_data_from_corleone__successful(self, client, successful_full_response):
        res = await client.get(URL, headers=HEADERS)
        documents = res.json()
        assert documents == successful_full_response

    @pytest.mark.usefixtures("successful_corleone_response", "successful_doc_type_response")
    async def test_documents__valid_cache(
        self,
        client,
        document_type_source_cache,
        document_type_code_cache,
        document_type_extraction_type_cache,
        rare_caches,
    ):
        document_type_source_cache.clear()
        document_type_code_cache.clear()
        document_type_extraction_type_cache.clear()
        rare_caches.clear()
        res = await client.get(URL, headers=HEADERS)
        document = res.json()["result"][0]

        assert rare_caches[RareCacheKeys.STATES.value] == DOCUMENT_STATES_RESPONSE
        assert rare_caches[RareCacheKeys.ENGINES.value] == OCR_ENGINES_RESPONSE
        assert rare_caches[RareCacheKeys.LANGUAGES.value] == OCR_LANGUAGES_RESPONSE
        assert document_type_source_cache["111"] == DocumentTypeSource.CORLEONE
        assert document_type_source_cache["1"] == DocumentTypeSource.DOCUMENT_TYPE
        assert document_type_code_cache[document["id"]] == document["documentType"]["code"]
        assert document_type_extraction_type_cache["111"] == "ml"

    @pytest.mark.parametrize(
        "query",
        [
            "page=0",
            "page=-1",
            "perPage=-1",
            "filterIds=10.2",
            "filterIds=stringId",
            "filterIds=",
        ],
    )
    async def test_get_document_list_invalid_params(self, client, query):
        document_service_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents"

        with aioresponses() as mock_response:
            mock_response.get(
                f"{document_service_url}?{query}",
                body=DOCUMENT_LIST_RESPONSE_JSON,
            )

            response = await client.get(f"{BASE_API_V5_PREFIX}/documents?{query}")
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_extract_data__ok(self, client: AsyncClient, document_id: str) -> None:
        document_url = f"{DOCUMENT_SERVICE_BASE_V1_URL}/documents/extract-data"
        data = {"documentIds": [document_id], "engineName": "TESSERACT"}

        with aioresponses() as mock_response:
            mock_response.post(url=document_url, status=HTTPStatus.OK, body=json.dumps([DOCUMENT_DETAIL_RESPONSE_DICT]))
            response = await client.post(f"{BASE_API_V5_PREFIX}/documents/extract-data", json=data)

            assert response.status_code == HTTPStatus.OK
            assert response.json() == [DOCUMENT_DETAIL_RESPONSE_DICT]
