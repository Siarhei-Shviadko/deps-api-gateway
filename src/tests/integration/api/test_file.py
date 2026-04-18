import json
import urllib
import uuid
from http import HTTPStatus

import pytest
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    FILES_BASE_API_PREFIX,
    FILES_ROUTER_PREFIX,
    V1_PREFIX,
)
from tests.data.file_json_data import (
    CLASSIFY_EXISTING_FILE_ERROR_RESPONSE,
    CLASSIFY_FILE_ERROR_RESPONSE,
    CLASSIFY_FILE_SUCCESS_RESPONSE,
    CREATE_BATCH_FROM_FILE_ERROR_RESPONSE,
    CREATE_BATCH_FROM_FILE_SUCCESS_RESPONSE,
    CREATE_DOCUMENT_FROM_FILE_ERROR_RESPONSE,
    CREATE_DOCUMENT_FROM_FILE_SUCCESS_RESPONSE,
    GET_FILE_NOT_FOUND_RESPONSE,
    GET_FILE_SERVER_ERROR_RESPONSE,
    GET_FILE_SUCCESS_RESPONSE,
    GET_FILES_RESPONSE,
    PROCESS_FILE_SUCCESS_RESPONSE,
    RESTART_FILE_ERROR_RESPONSE,
    RESTART_FILE_SUCCESS_RESPONSE,
    SPLIT_FILE_ERROR_RESPONSE,
    SPLIT_FILE_SUCCESS_RESPONSE,
)

API_GATEWAY_FILES_V5_URL = f"{BASE_API_V5_PREFIX}/files"
FILES_BASE_V1_URL = f"{FILES_BASE_API_PREFIX}{V1_PREFIX}/files"


@pytest.mark.asyncio
@pytest.mark.files
async def test_list_files__with_reference_params__ok(client: AsyncClient):
    params = {
        "name": "report",
        "state": ["new", "completed"],
        "dateStart": "2025-01-01T00:00:00Z",
        "dateEnd": "2025-12-31T23:59:59Z",
        "page": 0,
        "perPage": 10,
        "sortBy": "createdAt",
        "sortOrder": "desc",
        "referenceAvailable": False,
        "reference": "ref",
    }

    backend_params = {
        "name": params["name"],
        "state": params["state"],
        "dateStart": params["dateStart"],
        "dateEnd": params["dateEnd"],
        "page": params["page"],
        "perPage": params["perPage"],
        "sortBy": params["sortBy"],
        "sortOrder": params["sortOrder"],
        "referenceAvailable": str(params["referenceAvailable"]).lower(),
        "reference": params["reference"],
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}?{urllib.parse.urlencode(backend_params, doseq=True)}",
            status=HTTPStatus.OK,
            body=json.dumps(GET_FILES_RESPONSE),
        )

        response = await client.get(
            API_GATEWAY_FILES_V5_URL,
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_FILES_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_list_files__ok(client: AsyncClient):
    params = {
        "name": "report",
        "state": ["new", "completed"],
        "dateStart": "2025-01-01T00:00:00Z",
        "dateEnd": "2025-12-31T23:59:59Z",
        "page": 0,
        "perPage": 10,
        "sortBy": "createdAt",
        "sortOrder": "desc",
    }

    backend_params = {
        "name": params["name"],
        "state": params["state"],
        "dateStart": params["dateStart"],
        "dateEnd": params["dateEnd"],
        "page": params["page"],
        "perPage": params["perPage"],
        "sortBy": params["sortBy"],
        "sortOrder": params["sortOrder"],
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}?{urllib.parse.urlencode(backend_params, doseq=True)}",
            status=HTTPStatus.OK,
            body=json.dumps(GET_FILES_RESPONSE),
        )

        response = await client.get(
            API_GATEWAY_FILES_V5_URL,
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_FILES_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_list_files__reference_params_only__ok(client: AsyncClient):
    params = {
        "referenceAvailable": True,
        "reference": "ABC123",
    }

    backend_params = {
        "sortBy": "createdAt",
        "sortOrder": "desc",
        "referenceAvailable": str(params["referenceAvailable"]).lower(),
        "reference": params["reference"],
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(GET_FILES_RESPONSE),
        )

        response = await client.get(
            API_GATEWAY_FILES_V5_URL,
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_FILES_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_list_files__defaults__ok(client: AsyncClient):
    backend_params = {
        "sortBy": "createdAt",
        "sortOrder": "desc",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.OK,
            body=json.dumps(GET_FILES_RESPONSE),
        )

        response = await client.get(API_GATEWAY_FILES_V5_URL)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_FILES_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_list_files__error(client: AsyncClient):
    error_body = {"error": "Service unavailable"}

    backend_params = {
        "sortBy": "createdAt",
        "sortOrder": "desc",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}?{urllib.parse.urlencode(backend_params)}",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(error_body),
        )
        response = await client.get(API_GATEWAY_FILES_V5_URL)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == error_body


@pytest.mark.asyncio
@pytest.mark.files
async def test_get_file__success__returns_file_details(client: AsyncClient):
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}/{file_id}",
            status=HTTPStatus.OK,
            body=json.dumps(GET_FILE_SUCCESS_RESPONSE),
        )

        response = await client.get(f"{API_GATEWAY_FILES_V5_URL}/{file_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == GET_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_get_file__not_found__returns_404(client: AsyncClient):
    file_id = "non-existent-file-id"

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}/{file_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(GET_FILE_NOT_FOUND_RESPONSE),
        )

        response = await client.get(f"{API_GATEWAY_FILES_V5_URL}/{file_id}")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == GET_FILE_NOT_FOUND_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_get_file__backend_server_error__returns_bad_gateway(client: AsyncClient):
    file_id = "file-with-server-error"

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}/{file_id}",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=json.dumps(GET_FILE_SERVER_ERROR_RESPONSE),
        )

        response = await client.get(f"{API_GATEWAY_FILES_V5_URL}/{file_id}")

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.files
async def test_get_file__backend_error__proxies_error_response(client: AsyncClient):
    file_id = "file-with-backend-error"
    backend_error = {
        "error": "Access denied",
        "code": "FORBIDDEN",
        "message": "You don't have permission to access this file",
    }

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}/{file_id}",
            status=HTTPStatus.FORBIDDEN,
            body=json.dumps(backend_error),
        )

        response = await client.get(f"{API_GATEWAY_FILES_V5_URL}/{file_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == backend_error


@pytest.mark.asyncio
@pytest.mark.files
async def test_get_file__with_uuid_file_id__success(client: AsyncClient):
    file_id = str(uuid.uuid4())

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}/{file_id}",
            status=HTTPStatus.OK,
            body=json.dumps({**GET_FILE_SUCCESS_RESPONSE, "id": file_id}),
        )

        response = await client.get(f"{API_GATEWAY_FILES_V5_URL}/{file_id}")

        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert response_data["id"] == file_id
        assert "tenantId" in response_data
        assert "name" in response_data
        assert "state" in response_data


@pytest.mark.asyncio
@pytest.mark.files
async def test_get_file__with_special_characters_in_id__success(client: AsyncClient):
    file_id = "file-123-abc_def"

    with aioresponses() as mock_response:
        mock_response.get(
            f"{FILES_BASE_V1_URL}/{file_id}",
            status=HTTPStatus.OK,
            body=json.dumps({**GET_FILE_SUCCESS_RESPONSE, "id": file_id}),
        )

        response = await client.get(f"{API_GATEWAY_FILES_V5_URL}/{file_id}")

        assert response.status_code == HTTPStatus.OK
        response_data = response.json()
        assert response_data["id"] == file_id


@pytest.mark.asyncio
@pytest.mark.files
async def test_process_file__success__full_workflow_params(client: AsyncClient):
    file_content = b"test file content"
    workflow_params = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr", "table_extraction"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api", "priority": "high"},
    }

    files = {"file": ("test-document.pdf", file_content, "application/pdf")}

    data = {
        "engine": workflow_params["engine"] or "",
        "language": workflow_params["language"] or "",
        "llmType": workflow_params["llmType"] or "",
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "labels": json.dumps(["urgent", "finance"]),
        "groupId": "group-456",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/process",
            status=HTTPStatus.CREATED,
            body=json.dumps(PROCESS_FILE_SUCCESS_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/process",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == PROCESS_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_process_file__success__minimal_workflow_params(client: AsyncClient):
    file_content = b"minimal test content"
    workflow_params = {
        "engine": None,
        "language": None,
        "llmType": None,
        "parsingFeatures": ["ocr"],
        "needsUnifier": False,
        "needsExtraction": False,
        "assignedToMe": True,
        "metadata": {},
    }

    files = {"file": ("minimal.pdf", file_content, "application/pdf")}

    data = {
        "engine": "",
        "language": "",
        "llmType": "",
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
    }

    minimal_response = {"id": "minimal-file-456"}

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/process",
            status=HTTPStatus.CREATED,
            body=json.dumps(minimal_response),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/process",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == minimal_response


@pytest.mark.asyncio
@pytest.mark.files
async def test_process_file__validation_error__missing_file(client: AsyncClient):
    # No files provided - file is required!
    data = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": json.dumps(["ocr"]),
        "needsUnifier": "True",
        "needsExtraction": "True",
        "assignedToMe": "False",
        "metadata": "{}",
    }

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/process",
        data=data,  # No files parameter!
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_process_file__backend_error(client: AsyncClient):
    file_content = b"test content"
    workflow_params = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api"},
    }

    files = {"file": ("test.pdf", file_content, "application/pdf")}

    data = {
        "engine": workflow_params["engine"],
        "language": workflow_params["language"],
        "llmType": workflow_params["llmType"],
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/process",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps({"error": "Backend processing failed"}),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/process",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_file__success__full_workflow_params(client: AsyncClient):
    file_content = b"test file content for classification"
    workflow_params = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr", "table_extraction"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api", "priority": "high"},
    }

    files = {"file": ("test-document.pdf", file_content, "application/pdf")}

    data = {
        "engine": workflow_params["engine"] or "",
        "language": workflow_params["language"] or "",
        "llmType": workflow_params["llmType"] or "",
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "labels": json.dumps(["urgent", "finance"]),
        "groupId": "group-456",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/classify",
            status=HTTPStatus.CREATED,
            body=json.dumps(CLASSIFY_FILE_SUCCESS_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/classify",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CLASSIFY_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_file__success__minimal_workflow_params(client: AsyncClient):
    file_content = b"minimal test content for classification"
    workflow_params = {
        "engine": None,
        "language": None,
        "llmType": None,
        "parsingFeatures": ["ocr"],
        "needsUnifier": False,
        "needsExtraction": False,
        "assignedToMe": True,
        "metadata": {},
    }

    files = {"file": ("minimal.pdf", file_content, "application/pdf")}

    data = {
        "engine": "",
        "language": "",
        "llmType": "",
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "groupId": "group-123",
    }

    minimal_response = {"id": "minimal-classified-file-456"}

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/classify",
            status=HTTPStatus.CREATED,
            body=json.dumps(minimal_response),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/classify",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == minimal_response


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_file__validation_error__missing_file(client: AsyncClient):
    # No files provided - file is required!
    data = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": json.dumps(["ocr"]),
        "needsUnifier": "True",
        "needsExtraction": "True",
        "assignedToMe": "False",
        "metadata": "{}",
        "groupId": "group-456",
    }

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/classify",
        data=data,  # No files parameter!
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_file__validation_error__missing_group_id(client: AsyncClient):
    file_content = b"test content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}

    # Missing groupId - required for classification!
    data = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": json.dumps(["ocr"]),
        "needsUnifier": "True",
        "needsExtraction": "True",
        "assignedToMe": "False",
        "metadata": "{}",
    }

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/classify",
        files=files,
        data=data,  # No groupId parameter!
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_file__backend_error(client: AsyncClient):
    file_content = b"test content for classification"
    workflow_params = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api"},
    }

    files = {"file": ("test.pdf", file_content, "application/pdf")}

    data = {
        "engine": workflow_params["engine"],
        "language": workflow_params["language"],
        "llmType": workflow_params["llmType"],
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "groupId": "invalid-group-id",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/classify",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(CLASSIFY_FILE_ERROR_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/classify",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == CLASSIFY_FILE_ERROR_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_delete_files__single_file__ok(client: AsyncClient):
    file_id = str(uuid.uuid4())

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{FILES_BASE_V1_URL}?ids={file_id}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(
            API_GATEWAY_FILES_V5_URL,
            params={"ids": [file_id]},
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.files
async def test_delete_files__multiple_files__ok(client: AsyncClient):
    file_ids = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{FILES_BASE_V1_URL}?{urllib.parse.urlencode([('ids', fid) for fid in file_ids])}",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.delete(
            API_GATEWAY_FILES_V5_URL,
            params={"ids": file_ids},
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.files
async def test_delete_files__backend_error__proxies_error(client: AsyncClient):
    file_id = str(uuid.uuid4())
    error_body = {"error": "File not found", "code": "FILE_NOT_FOUND"}

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{FILES_BASE_V1_URL}?ids={file_id}",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps(error_body),
        )

        response = await client.delete(
            API_GATEWAY_FILES_V5_URL,
            params={"ids": [file_id]},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == error_body


@pytest.mark.asyncio
@pytest.mark.files
async def test_delete_files__backend_server_error__returns_bad_gateway(client: AsyncClient):
    file_id = str(uuid.uuid4())
    error_body = {"error": "Internal server error"}

    with aioresponses() as mock_response:
        mock_response.delete(
            f"{FILES_BASE_V1_URL}?ids={file_id}",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=json.dumps(error_body),
        )

        response = await client.delete(
            API_GATEWAY_FILES_V5_URL,
            params={"ids": [file_id]},
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.files
async def test_delete_files__validation_error__missing_ids(client: AsyncClient):
    response = await client.delete(API_GATEWAY_FILES_V5_URL)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_delete_files__validation_error__empty_ids_list(client: AsyncClient):
    response = await client.delete(
        API_GATEWAY_FILES_V5_URL,
        params={"ids": []},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_existing_file__success__ok(client: AsyncClient):
    file_id = "file-123"
    workflow_params = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr", "table_extraction"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api"},
        "groupId": "group-456",
    }

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{FILES_BASE_V1_URL}/{file_id}/classify",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.patch(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/classify",
            json=workflow_params,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_existing_file__validation_error__missing_group_id(client: AsyncClient):
    file_id = "file-123"

    response = await client.patch(
        f"{API_GATEWAY_FILES_V5_URL}/{file_id}/classify",
        json={
            "parsingFeatures": ["ocr"],
            "needsUnifier": True,
            "needsExtraction": True,
            "assignedToMe": False,
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_existing_file__backend_error__proxies_error(client: AsyncClient):
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{FILES_BASE_V1_URL}/{file_id}/classify",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(CLASSIFY_EXISTING_FILE_ERROR_RESPONSE),
        )

        response = await client.patch(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/classify",
            json={
                "parsingFeatures": ["ocr"],
                "needsUnifier": True,
                "needsExtraction": True,
                "assignedToMe": False,
                "groupId": "invalid-group-id",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == CLASSIFY_EXISTING_FILE_ERROR_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_classify_existing_file__backend_server_error__returns_bad_gateway(client: AsyncClient):
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{FILES_BASE_V1_URL}/{file_id}/classify",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        response = await client.patch(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/classify",
            json={
                "parsingFeatures": ["ocr"],
                "needsUnifier": True,
                "needsExtraction": True,
                "assignedToMe": False,
                "groupId": "group-456",
            },
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_file__success__full_workflow_params(client: AsyncClient):
    file_content = b"test file content for splitting"
    workflow_params = {
        "documentTypeId": "document-type-123",
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr", "table_extraction"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api", "priority": "high"},
    }

    files = {"file": ("test-document.pdf", file_content, "application/pdf")}

    data = {
        "documentTypeId": workflow_params["documentTypeId"] or "",
        "classificationEnabled": True,
        "engine": workflow_params["engine"] or "",
        "language": workflow_params["language"] or "",
        "llmType": workflow_params["llmType"] or "",
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "labels": json.dumps(["urgent", "finance"]),
        "groupId": "group-456",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/split",
            status=HTTPStatus.CREATED,
            body=json.dumps(SPLIT_FILE_SUCCESS_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/split",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == SPLIT_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_file__success__minimal_workflow_params(client: AsyncClient):
    file_content = b"minimal test content for splitting"
    workflow_params = {
        "documentTypeId": None,
        "engine": None,
        "language": None,
        "llmType": None,
        "parsingFeatures": ["ocr"],
        "needsUnifier": False,
        "needsExtraction": False,
        "assignedToMe": True,
        "metadata": {},
    }

    files = {"file": ("minimal.pdf", file_content, "application/pdf")}

    data = {
        "documentTypeId": "",
        "classificationEnabled": True,
        "engine": "",
        "language": "",
        "llmType": "",
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "groupId": "group-123",
    }

    minimal_response = {"id": "minimal-splitted-file-456"}

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/split",
            status=HTTPStatus.CREATED,
            body=json.dumps(minimal_response),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/split",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == minimal_response


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_file__validation_error__missing_file(client: AsyncClient):
    # No files provided - file is required!
    data = {
        "classificationEnabled": "True",
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": json.dumps(["ocr"]),
        "needsUnifier": "True",
        "needsExtraction": "True",
        "assignedToMe": "False",
        "metadata": "{}",
        "groupId": "group-456",
    }

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/split",
        data=data,  # No files parameter!
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_file__validation_error__missing_group_id(client: AsyncClient):
    file_content = b"test content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}

    # Missing groupId - required for splitting!
    data = {
        "classificationEnabled": "True",
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": json.dumps(["ocr"]),
        "needsUnifier": "True",
        "needsExtraction": "True",
        "assignedToMe": "False",
        "metadata": "{}",
    }

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/split",
        files=files,
        data=data,  # No groupId parameter!
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_file__backend_error(client: AsyncClient):
    file_content = b"test content for splitting"
    workflow_params = {
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api"},
    }

    files = {"file": ("test.pdf", file_content, "application/pdf")}

    data = {
        "classificationEnabled": True,
        "engine": workflow_params["engine"],
        "language": workflow_params["language"],
        "llmType": workflow_params["llmType"],
        "parsingFeatures": json.dumps(workflow_params["parsingFeatures"]),
        "needsUnifier": str(workflow_params["needsUnifier"]),
        "needsExtraction": str(workflow_params["needsExtraction"]),
        "assignedToMe": str(workflow_params["assignedToMe"]),
        "metadata": json.dumps(workflow_params["metadata"]),
        "groupId": "invalid-group-id",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_API_PREFIX}{V1_PREFIX}{FILES_ROUTER_PREFIX}/split",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(SPLIT_FILE_ERROR_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/split",
            files=files,
            data=data,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == SPLIT_FILE_ERROR_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_existing_file__success__ok(client: AsyncClient):
    file_id = "file-123"
    workflow_params = {
        "documentTypeId": "document-type-id-456",
        "classificationEnabled": True,
        "engine": "ai-engine",
        "language": "en",
        "llmType": "gpt-4",
        "parsingFeatures": ["ocr", "table_extraction"],
        "needsUnifier": True,
        "needsExtraction": True,
        "assignedToMe": False,
        "metadata": {"source": "api"},
        "groupId": "group-789",
    }

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{FILES_BASE_V1_URL}/{file_id}/split",
            status=HTTPStatus.NO_CONTENT,
        )

        response = await client.patch(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/split",
            json=workflow_params,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_existing_file__validation_error__missing_group_id(client: AsyncClient):
    file_id = "file-123"

    response = await client.patch(
        f"{API_GATEWAY_FILES_V5_URL}/{file_id}/split",
        json={
            "classificationEnabled": True,
            "parsingFeatures": ["ocr"],
            "needsUnifier": True,
            "needsExtraction": True,
            "assignedToMe": False,
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_existing_file__backend_error__proxies_error(client: AsyncClient):
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{FILES_BASE_V1_URL}/{file_id}/split",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(SPLIT_FILE_ERROR_RESPONSE),
        )

        response = await client.patch(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/split",
            json={
                "classificationEnabled": True,
                "parsingFeatures": ["ocr"],
                "needsUnifier": True,
                "needsExtraction": True,
                "assignedToMe": False,
                "groupId": "invalid-group-id",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == SPLIT_FILE_ERROR_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_split_existing_file__backend_server_error__returns_bad_gateway(client: AsyncClient):
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.patch(
            f"{FILES_BASE_V1_URL}/{file_id}/split",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        response = await client.patch(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/split",
            json={
                "classificationEnabled": True,
                "parsingFeatures": ["ocr"],
                "needsUnifier": True,
                "needsExtraction": True,
                "assignedToMe": False,
                "groupId": "group-456",
            },
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_document_from_file__success__ok(client: AsyncClient):
    file_id = "file-123"
    document_type_id = "document-type-456"

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/create-document",
            status=HTTPStatus.CREATED,
            body=json.dumps(CREATE_DOCUMENT_FROM_FILE_SUCCESS_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-document",
            json={"documentTypeId": document_type_id},
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_DOCUMENT_FROM_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_document_from_file__validation_error__missing_document_type(client: AsyncClient):
    file_id = "file-123"

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-document",
        json={},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_document_from_file__backend_error__proxies_error(client: AsyncClient):
    file_id = "file-123"
    document_type_id = "invalid-document-type"

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/create-document",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(CREATE_DOCUMENT_FROM_FILE_ERROR_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-document",
            json={"documentTypeId": document_type_id},
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == CREATE_DOCUMENT_FROM_FILE_ERROR_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_document_from_file__backend_server_error__returns_bad_gateway(client: AsyncClient):
    file_id = "file-123"
    document_type_id = "document-type-456"

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/create-document",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-document",
            json={"documentTypeId": document_type_id},
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_document_from_file__file_not_found__returns_404(client: AsyncClient):
    file_id = "non-existent-file-id"
    document_type_id = "document-type-456"

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/create-document",
            status=HTTPStatus.NOT_FOUND,
            body=json.dumps({"error": "File not found", "code": "FILE_NOT_FOUND"}),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-document",
            json={"documentTypeId": document_type_id},
        )

        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_batch_from_file__success__ok(client: AsyncClient) -> None:
    file_id = "file-123"
    request_body = {
        "batchName": "Test Batch",
        "files": [
            {
                "name": "test.pdf",
                "path": "/test.pdf",
                "documentTypeId": None,
            },
        ],
        "groupId": "group id",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/create-batch",
            status=HTTPStatus.CREATED,
            body=json.dumps(CREATE_BATCH_FROM_FILE_SUCCESS_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-batch",
            json=request_body,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == CREATE_BATCH_FROM_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_batch_from_file__validation_error__missing_fields(client: AsyncClient) -> None:
    file_id = "file-123"

    response = await client.post(
        f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-batch",
        json={},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.files
async def test_create_batch_from_file__backend_error__proxies_error(client: AsyncClient) -> None:
    file_id = "file-123"
    request_body = {
        "batchName": "Test Batch",
        "files": [
            {
                "name": "test.pdf",
                "path": "/test.pdf",
                "documentTypeId": "invalid-type",
            },
        ],
        "groupId": "group id",
    }

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/create-batch",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(CREATE_BATCH_FROM_FILE_ERROR_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/create-batch",
            json=request_body,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == CREATE_BATCH_FROM_FILE_ERROR_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_restart_file__success__ok(client: AsyncClient) -> None:
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/restart",
            status=HTTPStatus.OK,
            body=json.dumps(RESTART_FILE_SUCCESS_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/restart",
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == RESTART_FILE_SUCCESS_RESPONSE


@pytest.mark.asyncio
@pytest.mark.files
async def test_restart_file__backend_error__proxies_error(client: AsyncClient) -> None:
    file_id = "file-123"

    with aioresponses() as mock_response:
        mock_response.post(
            f"{FILES_BASE_V1_URL}/{file_id}/restart",
            status=HTTPStatus.BAD_REQUEST,
            body=json.dumps(RESTART_FILE_ERROR_RESPONSE),
        )

        response = await client.post(
            f"{API_GATEWAY_FILES_V5_URL}/{file_id}/restart",
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == RESTART_FILE_ERROR_RESPONSE
