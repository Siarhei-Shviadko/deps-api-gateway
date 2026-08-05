from http import HTTPStatus

import pytest
from aioresponses import aioresponses

from deps_api_gateway.constants import (
    AI_FUSION_BASE_PREFIX,
    BASE_API_V5_PREFIX,
    V1_PREFIX,
)
from tests.data.ai_fusion_json_data import (
    AI_FUSION_ATTACH_LLM_EXTRACTOR_REQUEST,
    AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_DICT,
    AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_JSON,
    AI_FUSION_AVAILABLE_MODELS_RESPONSE_DICT,
    AI_FUSION_AVAILABLE_MODELS_RESPONSE_JSON,
    AI_FUSION_COMPLETION_CREATE_REQUEST,
    AI_FUSION_COMPLETION_CREATED_RESPONSE_DATA_DICT,
    AI_FUSION_COMPLETION_CREATED_RESPONSE_JSON,
    AI_FUSION_CONVERSATION_GET_RESPONSE_DATA_DICT,
    AI_FUSION_CONVERSATION_GET_RESPONSE_JSON,
    AI_FUSION_CREATE_QUERY_REQUEST,
    AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_DICT,
    AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_JSON,
    AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT,
    AI_FUSION_SERIALIZED_QUERY_RESPONSE_JSON,
    AI_FUSION_UPDATE_LLM_EXTRACTOR_REQUEST,
)

AI_FUSION_BASE_URL = f"{AI_FUSION_BASE_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_create_completion__ok(client):
    fusion_url = f"{AI_FUSION_BASE_URL}/conversations/document-id"

    with aioresponses() as mock_response:
        mock_response.put(fusion_url, body=AI_FUSION_COMPLETION_CREATED_RESPONSE_JSON, status=HTTPStatus.CREATED)

        response = await client.put(
            f"{BASE_API_V5_PREFIX}/documents/document-id/conversation",
            json=AI_FUSION_COMPLETION_CREATE_REQUEST,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == AI_FUSION_COMPLETION_CREATED_RESPONSE_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_remove_completions__no_content(client, document_id, completion_code):
    fusion_url = f"{AI_FUSION_BASE_URL}/conversations/{document_id}/completions?completionCodes={completion_code}"

    with aioresponses() as mock_response:
        mock_response.delete(fusion_url, status=HTTPStatus.NO_CONTENT)

        data = {"completionCodes": [completion_code]}

        response = await client.delete(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/conversation/completions",
            params=data,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_create_getting_conversation__ok(client):
    fusion_url = f"{AI_FUSION_BASE_URL}/conversations/document-id"

    with aioresponses() as mock_response:
        mock_response.get(fusion_url, body=AI_FUSION_CONVERSATION_GET_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.get(f"{BASE_API_V5_PREFIX}/documents/document-id/conversation")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_CONVERSATION_GET_RESPONSE_DATA_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_clear_conversation__no_content(client, document_id):
    fusion_url = f"{AI_FUSION_BASE_URL}/conversations/{document_id}"

    with aioresponses() as mock_response:
        mock_response.delete(fusion_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(f"{BASE_API_V5_PREFIX}/documents/{document_id}/conversation")

        assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_llms(client):
    fusion_url = f"{AI_FUSION_BASE_URL}/analysis/models"

    with aioresponses() as mock_response:
        mock_response.get(fusion_url, body=AI_FUSION_AVAILABLE_MODELS_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.get(f"{BASE_API_V5_PREFIX}/tools/llms")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_AVAILABLE_MODELS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_retrieve_insights__ok(client, document_id: str):
    fusion_url = f"{AI_FUSION_BASE_URL}/analysis/retrieve-insights"

    data = {
        "model": "model",
        "requestedInsights": {
            "code": "prompt",
            "anotherCode": {
                "workflow": {
                    "prompts": [{"content": "prompt1"}, {"content": "prompt2"}],
                    "responseModel": {"type": "object", "properties": {"key": {"type": "string"}}},
                },
            },
        },
        "customInstructions": "instructions",
        "params": {
            "temperature": 0,
            "topP": 1,
            "groupingFactor": 5,
            "maxTokens": 2048,
            "stop": ["END", "\n"],
            "seed": 42,
            "logprobs": False,
            "extraModelParams": {"n": 5},
        },
        "files": ["file1.png", "file2.png"],
    }

    with aioresponses() as mock_response:
        mock_response.post(fusion_url, body=AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/documents/{document_id}/analysis/retrieve-insights",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_retrieve_file_insights__ok(client):
    fusion_url = f"{AI_FUSION_BASE_URL}/analysis/retrieve-file-insights"

    data = {
        "model": "model",
        "filePath": "some/random/path.pdf",
        "requestedInsights": {
            "code": "prompt",
        },
        "customInstructions": "instructions",
        "params": {
            "temperature": 0,
            "topP": 1,
            "groupingFactor": 5,
            "maxTokens": 2048,
            "stop": ["END", "\n"],
            "seed": 42,
            "logprobs": False,
            "extraModelParams": {"n": 5},
        },
        "files": ["file1.png", "file2.png"],
    }

    with aioresponses() as mock_response:
        mock_response.post(fusion_url, body=AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/analysis/retrieve-file-insights",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_RETRIEVE_INSIGHTS_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_add_extraction_query__created(client, document_type_id: str, extractor_id: str):
    fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors/{extractor_id}/query"

    with aioresponses() as mock_response:
        mock_response.post(fusion_url, body=AI_FUSION_SERIALIZED_QUERY_RESPONSE_JSON, status=HTTPStatus.CREATED)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/llm-extractors/{extractor_id}/extraction-query",
            json=AI_FUSION_CREATE_QUERY_REQUEST,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_update_extraction_query__ok(client, document_type_id: str, extractor_id: str):
    code = AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT["code"]

    fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors/{extractor_id}/query/{code}"

    with aioresponses() as mock_response:
        mock_response.patch(fusion_url, body=AI_FUSION_SERIALIZED_QUERY_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}"
            f"/llm-extractors/{extractor_id}/extraction-query/{code}",
            json={"workflow": AI_FUSION_CREATE_QUERY_REQUEST["workflow"]},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_SERIALIZED_QUERY_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_attach_llm_extractor__ok(client):
    fusion_url = f"{AI_FUSION_BASE_URL}/document-types/llm-extractors"

    with aioresponses() as mock_response:
        mock_response.post(fusion_url, body=AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_JSON, status=HTTPStatus.CREATED)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/llm-extractor",
            json=AI_FUSION_ATTACH_LLM_EXTRACTOR_REQUEST,
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_update_llm_extractor__ok(client, document_type_id: str, extractor_id: str):
    fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors/{extractor_id}"

    with aioresponses() as mock_response:
        mock_response.put(fusion_url, body=AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.put(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/llm-extractors/{extractor_id}",
            json=AI_FUSION_UPDATE_LLM_EXTRACTOR_REQUEST,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_assign_llm_to_llm_extractor__ok(client, document_type_id: str, extractor_id: str):
    fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors/{extractor_id}/llm"

    data = {"provider": "dial", "model": "epam.dial-rag"}

    with aioresponses() as mock_response:
        mock_response.put(fusion_url, body=AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_JSON, status=HTTPStatus.OK)

        response = await client.put(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/llm-extractors/{extractor_id}/llm",
            json=data,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == AI_FUSION_ATTACH_LLM_EXTRACTOR_RESPONSE_DICT


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_move_queries_between_extractors__ok(client, document_type_id: str):
    fusion_url = f"{AI_FUSION_BASE_URL}/document-types/{document_type_id}/llm-extractors/move-queries"

    request_payload = {
        "sourceExtractorId": "source_extractor_id",
        "targetExtractorId": "target_extractor_id",
        "fieldsCodes": ["field_a", "field_b"],
    }

    with aioresponses() as mock_response:
        mock_response.post(fusion_url, status=HTTPStatus.OK)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/document-types/{document_type_id}/llm-extractors/move-queries",
            json=request_payload,
        )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
@pytest.mark.ai_fusion
async def test_add_llm_coordinates__ok(client, document_id: str):
    fusion_url = f"{AI_FUSION_BASE_URL}/llm-coordinates/{document_id}"

    request_payload = {
        "fieldCodes": ["field_a", "field_b"],
    }

    with aioresponses() as mock_response:
        mock_response.post(fusion_url, status=HTTPStatus.OK)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/llm-coordinates/{document_id}",
            json=request_payload,
        )

    assert response.status_code == HTTPStatus.OK
