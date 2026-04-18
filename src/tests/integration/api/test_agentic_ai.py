import json
import re
import uuid
from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch
from urllib.parse import urlencode

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses
from httpx import AsyncClient

from deps_api_gateway.constants import (
    AGENTIC_AI_BASE_API_PREFIX,
    BASE_API_V5_PREFIX,
    V1_PREFIX,
)
from deps_api_gateway.infrastructure import AgenticAISSEProxy
from tests.data.agentic_ai_json_data import (
    GET_AGENT_VENDORS_RESPONSE,
    GET_CONVERSATION_COMPLETIONS_RESPONSE,
)

AGENTIC_AI_BASE_URL = f"{AGENTIC_AI_BASE_API_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
async def test_create_agent_vendor__201_status(client: AsyncClient):
    url = f"{AGENTIC_AI_BASE_URL}/agent-vendors"
    payload = {
        "name": "test_name",
        "description": "test_desc",
        "baseUrl": "http://base_url",
        "avatarUrl": "http://avatar_url",
    }
    expected_response = {"id": uuid.uuid4().hex}

    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.CREATED, body=json.dumps(expected_response))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/agentic-ai/agent-vendors",
            json=payload,
        )

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_agentic_ai__service_unavailable__502_status(client: AsyncClient):
    url = f"{AGENTIC_AI_BASE_URL}/agent-vendors"
    payload = {
        "name": "test_name",
        "description": "test_desc",
        "baseUrl": "http://base_url",
        "avatarUrl": "http://avatar_url",
    }

    with aioresponses() as mock_response:
        mock_response.post(url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/agentic-ai/agent-vendors",
            json=payload,
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_get_agent_vendors__200_status(client: AsyncClient):
    url = f"{AGENTIC_AI_BASE_URL}/agent-vendors"

    with aioresponses() as mock_response:
        mock_response.get(url, status=HTTPStatus.OK, body=json.dumps(GET_AGENT_VENDORS_RESPONSE))

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/agentic-ai/agent-vendors",
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == GET_AGENT_VENDORS_RESPONSE


@pytest.mark.asyncio
async def test_activate_agent_vendor__204_status(client: AsyncClient):
    agent_vendor_id = uuid.uuid4().hex
    url = f"{AGENTIC_AI_BASE_URL}/agent-vendors/{agent_vendor_id}/activate"

    with aioresponses() as mock_response:
        mock_response.patch(url, status=HTTPStatus.NO_CONTENT)

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/agentic-ai/agent-vendors/{agent_vendor_id}/activate",
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_create_conversation__201_status(client: AsyncClient):
    url = f"{AGENTIC_AI_BASE_URL}/conversations"
    payload = {
        "agentVendorId": "test_agent_vendor_id",
        "modeId": "test_mode_id",
        "title": "test_title",
        "arguments": {
            "tool_set_code_1": {
                "tool_code_1": [
                    {"parameter": "param_1", "value": "value_1"},
                    {"parameter": "param_2", "value": "value_2"},
                ],
            }
        },
        "relation": {"document_id": "abc"},
    }
    expected_response = {"id": uuid.uuid4().hex}

    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.CREATED, body=json.dumps(expected_response))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/agentic-ai/conversations",
            json=payload,
        )

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_conversation__200_status(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    url = f"{AGENTIC_AI_BASE_URL}/conversations/{conversation_id}"

    expected_response = {
        "id": conversation_id,
        "title": "Test Conversation 1",
        "relation": {"details": None},
        "completions": [
            {
                "id": uuid.uuid4().hex,
                "question": {"text": "Test Question 1", "createdAt": str(datetime.now())},
                "executionContext": [{"text": "Test Execution Context 1"}],
                "answer": {"text": "Test Answer 1", "createdAt": str(datetime.now())},
            }
        ],
    }

    with aioresponses() as mock_response:
        mock_response.get(url, status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.get(f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}")

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()

        json_response = response.json()
        assert json_response == expected_response


@pytest.mark.asyncio
async def test_get_conversations__200_status(client):
    expected_response = {
        "items": [
            {
                "id": uuid.uuid4().hex,
                "agent_vendor_id": uuid.uuid4().hex,
                "mode": {
                    "id": uuid.uuid4().hex,
                    "code": "default",
                },
                "context": {"tools": {}},
                "relation": {"details": {}},
                "title": "Conversation 1",
                "created_by": uuid.uuid4().hex,
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
            },
            {
                "id": uuid.uuid4().hex,
                "agent_vendor_id": uuid.uuid4().hex,
                "mode": {
                    "id": uuid.uuid4().hex,
                    "code": "advanced",
                },
                "context": {"tools": {}},
                "relation": {"details": {}},
                "title": "Conversation 2",
                "created_by": uuid.uuid4().hex,
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
            },
        ],
        "total": 2,
    }

    query_params = {"page": 1, "size": 10, "sort_by": "created_at", "sort_order": "desc"}

    with aioresponses() as mock_response:
        mock_response.get(re.compile(r".*/conversations"), status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/agentic-ai/conversations",
            params=query_params,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()

        json_response = response.json()
        assert json_response == expected_response


@pytest.mark.asyncio
async def test_get_conversation_completions__200_status(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    base_url = f"{AGENTIC_AI_BASE_URL}/conversations/{conversation_id}/completions"
    params = {"page": 2, "perPage": 2}
    encoded_params = urlencode(params)
    url = f"{base_url}?{encoded_params}"

    with aioresponses() as mock_response:
        mock_response.get(url, status=HTTPStatus.OK, body=json.dumps(GET_CONVERSATION_COMPLETIONS_RESPONSE))
        response = await client.get(
            f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}/completions",
            params=params,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == GET_CONVERSATION_COMPLETIONS_RESPONSE


@pytest.mark.asyncio
async def test_update_conversation__200_status(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    url = f"{AGENTIC_AI_BASE_URL}/conversations/{conversation_id}"
    payload = {"title": "Updated Title"}
    expected_response = {"id": conversation_id}

    with aioresponses() as mock_response:
        mock_response.patch(url, status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.patch(
            f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}",
            json=payload,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_delete_conversations__204_status(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    url = f"{AGENTIC_AI_BASE_URL}/conversations?id={conversation_id}"

    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.NO_CONTENT)

        params = {"id": [conversation_id]}

        response = await client.delete(
            f"{BASE_API_V5_PREFIX}/agentic-ai/conversations",
            params=params,
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_response.assert_called_once()


@pytest.mark.asyncio
async def test_chat__200_status(client: AsyncClient):
    conversation_id = uuid.uuid4().hex

    async def mock_chat_generator(*args, **kwargs):
        yield b"event: message\n"
        yield b'data: {"text": "Hello"}\n\n'

    with patch.object(AgenticAISSEProxy, "chat", return_value=mock_chat_generator()):
        url = f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}/chat"
        response = await client.get(url, params={"userQuestion": "test_question"})

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_chat__error_occured__error_event_in_response(client: AsyncClient):
    conversation_id = uuid.uuid4().hex

    with patch.object(AgenticAISSEProxy, "chat", side_effect=Exception("Error occurred")):
        url = f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}/chat"
        response = await client.get(url, params={"userQuestion": "test_question"})

        assert response.status_code == HTTPStatus.OK

        splited_response_message = response.text.split("\n")
        assert splited_response_message[0] == "event: error"
        assert splited_response_message[1] == 'data: {"type": "Error", "text": "An unexpected error occurred"}'


@pytest.mark.asyncio
async def test_chat__invalid_json_arguments__error_code_in_response(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    url = f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}/chat"

    response = await client.get(url, params={"userQuestion": "test_question", "arguments": "{invalid json}"})

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response_data = response.json()
    assert response_data["code"] == "illegal_argument"
    assert "Invalid JSON format for arguments" in response_data["message"]


@pytest.mark.asyncio
async def test_edit_question__200_status(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    completion_id = uuid.uuid4().hex

    async def mock_chat_generator(*args, **kwargs):
        yield b"event: message\n"
        yield b'data: {"text": "Hello"}\n\n'

    with patch.object(AgenticAISSEProxy, "edit_question", return_value=mock_chat_generator()):
        url = f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}/completions/{completion_id}"
        response = await client.patch(url, params={"userQuestion": "edited question"})

        assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_edit_question__error_occured__error_event_in_response(client: AsyncClient):
    conversation_id = uuid.uuid4().hex
    completion_id = uuid.uuid4().hex

    with patch.object(AgenticAISSEProxy, "edit_question", side_effect=Exception("Error occurred")):
        url = f"{BASE_API_V5_PREFIX}/agentic-ai/conversations/{conversation_id}/completions/{completion_id}"
        response = await client.patch(url, params={"userQuestion": "edited question"})

        assert response.status_code == HTTPStatus.OK

        splited_response_message = response.text.split("\n")
        assert splited_response_message[0] == "event: error"
        assert splited_response_message[1] == 'data: {"type": "Error", "text": "An unexpected error occurred"}'


@pytest.mark.asyncio
async def test_get_modes__200_status(client):
    expected_response = {
        "modes": [
            {
                "id": uuid.uuid4().hex,
                "code": "document",
                "toolSets": [
                    {
                        "id": uuid.uuid4().hex,
                        "code": "genai-queries-agent",
                        "name": "GenAI Queries Agent",
                        "tools": [
                            {
                                "code": "load-document-layout",
                                "name": "Load Document Layout",
                                "parameters": [{"name": "document_id"}],
                            }
                        ],
                    }
                ],
            }
        ]
    }

    with aioresponses() as mock_response:
        mock_response.get(f"{AGENTIC_AI_BASE_URL}/modes", status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/agentic-ai/modes",
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()

        assert response.json() == expected_response
