import json
import uuid
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses
from async_rest_client.constants import Methods
from httpx import AsyncClient
from yarl import URL

from deps_api_gateway.application.types import InvitationSortingField, UserSortingField
from deps_api_gateway.constants import (
    BASE_API_V5_PREFIX,
    IAM_BASE_API_PREFIX,
    V1_PREFIX,
)
from tests.data.iam_json_data import (
    ORGANISATION_DICT,
    ORGANISATION_INVITEES_DICT,
    ORGANISATION_INVITEES_JSON,
    ORGANISATION_JSON,
    ORGANISATION_USERS_DICT,
    ORGANISATION_USERS_JSON,
    ORGANISATIONS_DICT,
    ORGANISATIONS_JSON,
    USER_DICT,
    USER_JSON,
)

IAM_BASE_URL = f"{IAM_BASE_API_PREFIX}{V1_PREFIX}"


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_activate_user_organisation__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/activate"
    expected_payload = {"pk": tenant_id, "name": "TestName", "customizationUrl": None}
    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.OK, body=json.dumps(expected_payload))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/activate",
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_activate_user_organisation__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/activate"

    with aioresponses() as mock_response:
        mock_response.post(url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/activate",
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_invite_user_to_organisation__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/invite"
    expected_payload = [{"email": "abc@test.ru"}]
    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.OK, body=json.dumps(expected_payload))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/invite",
            json=expected_payload,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.POST, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_invite_user_to_organisation__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/invite"
    expected_payload = [{"email": "abc@test.ru"}]
    with aioresponses() as mock_response:
        mock_response.post(url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/invite",
            json=expected_payload,
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_join_to_organisation__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/join"
    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.OK)

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/join",
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_join_to_organisation__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/join"
    with aioresponses() as mock_response:
        mock_response.post(url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/join",
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_approve_user_requests__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/approve"
    user_id = uuid.uuid4().hex
    expected_payload = {"userPks": [user_id]}
    expected_response = {"approvedUsers": [user_id]}
    with aioresponses() as mock_response:
        mock_response.post(url, status=HTTPStatus.OK, body=json.dumps(expected_response))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/approve",
            json={"userIds": [user_id]},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.POST, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_approve_user_requests__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/approve"
    user_id = uuid.uuid4().hex
    with aioresponses() as mock_response:
        mock_response.post(url, exception=ClientConnectionError("failed_connection"))

        response = await client.post(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/approve",
            json={"userIds": [user_id]},
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_user_requests__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/approvals"
    user_id = uuid.uuid4().hex
    expected_payload = {"declinedUsers": [user_id]}
    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.OK, body=json.dumps(expected_payload))

        response = await client.request(
            "DELETE",
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/approvals",
            json={"userIds": [user_id]},
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_user_requests__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/approvals"
    user_id = uuid.uuid4().hex

    with aioresponses() as mock_response:
        mock_response.delete(url, exception=ClientConnectionError("failed_connection"))

        response = await client.request(
            "DELETE",
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/approvals",
            json={"userIds": [user_id]},
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_users_from_organisation__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/users"
    user_id = uuid.uuid4().hex
    expected_payload = {"users": [user_id]}
    with aioresponses() as mock_response:
        mock_response.delete(url, exception=ClientConnectionError("failed_connection"))

        response = await client.request(
            "DELETE",
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/users",
            json={"userIds": [user_id]},
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.DELETE, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_users_from_organisation__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/users"
    user_id = uuid.uuid4().hex
    expected_payload = {"users": [user_id]}
    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.OK, body=json.dumps({"deletedUsers": [user_id]}))

        response = await client.request(
            "DELETE",
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/users",
            json={"userIds": [user_id]},
        )

        assert response.status_code == HTTPStatus.OK
        assert user_id in response.json()["deletedUsers"]
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.DELETE, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_invitees__200_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/invitees"
    invitee_email = "half_invite@tets.ru"
    expected_payload = {"invitees": [invitee_email]}
    with aioresponses() as mock_response:
        mock_response.delete(url, status=HTTPStatus.OK)

        response = await client.request(
            "DELETE",
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/invitees",
            json={"invitees": [invitee_email]},
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.DELETE, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_invitees__service_unavailable__502_status(client: AsyncClient, tenant_id):
    url = f"{IAM_BASE_URL}/organisations/{tenant_id}/invitees"
    invitee_email = "half_invite@tets.ru"
    expected_payload = {"invitees": [invitee_email]}
    with aioresponses() as mock_response:
        mock_response.delete(url, exception=ClientConnectionError("failed_connection"))

        response = await client.request(
            "DELETE",
            f"{BASE_API_V5_PREFIX}/iam/organisations/{tenant_id}/invitees",
            json={"invitees": [invitee_email]},
        )

        assert response.status_code == HTTPStatus.BAD_GATEWAY
        mock_response.assert_called_once()
        assert mock_response.requests.get((Methods.DELETE, URL(url)))[0].kwargs["json"] == expected_payload


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_create_user(client: AsyncClient, organisation_id: str):
    iam_url = f"{IAM_BASE_URL}/users"
    data = {
        "user": {
            "email": "email@mail.com",
            "username": "username",
            "firstName": "firstName",
            "lastName": "lastName",
            "organisation": organisation_id,
        },
        "createAPIKey": True,
    }

    with aioresponses() as mock_response:
        mock_response.post(iam_url, status=HTTPStatus.CREATED, body=USER_JSON)

        response = await client.post(f"{BASE_API_V5_PREFIX}/iam/users", json=data)

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()
        assert response.json() == USER_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_current_user(client: AsyncClient):
    iam_url = f"{IAM_BASE_URL}/users/me"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=USER_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/iam/users/me")

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == USER_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_or_create_user_api_key(client: AsyncClient):
    iam_url = f"{IAM_BASE_URL}/users/me/api-key"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=b'"api-key-string"')

        response = await client.get(f"{BASE_API_V5_PREFIX}/iam/users/me/api-key")

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == "api-key-string"


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_revoke_user_api_key(client: AsyncClient):
    iam_url = f"{IAM_BASE_URL}/users/me/api-key"

    with aioresponses() as mock_response:
        mock_response.delete(iam_url, status=HTTPStatus.NO_CONTENT)

        response = await client.delete(f"{BASE_API_V5_PREFIX}/iam/users/me/api-key")

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_user(client: AsyncClient, user_id: str):
    iam_url = f"{IAM_BASE_URL}/users/{user_id}"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=USER_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/iam/users/{user_id}")

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == USER_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_organisations(client: AsyncClient):
    iam_url = f"{IAM_BASE_URL}/organisations"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=ORGANISATIONS_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/iam/organisations")

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == ORGANISATIONS_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_organisation_details(client: AsyncClient, organisation_id: str):
    iam_url = f"{IAM_BASE_URL}/organisations/{organisation_id}"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=ORGANISATION_JSON)

        response = await client.get(f"{BASE_API_V5_PREFIX}/iam/organisations/{organisation_id}")

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == ORGANISATION_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_organisation_users(client: AsyncClient, organisation_id: str):
    data = {
        "page": 1,
        "perPage": 10,
        "fullName": "",
        "sortBy": UserSortingField.FULL_NAME_ASC.value,
    }

    iam_url = f"{IAM_BASE_URL}/organisations/{organisation_id}/users?{urlencode(data)}"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=ORGANISATION_USERS_JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{organisation_id}/users",
            params=data,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == ORGANISATION_USERS_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_organisation_invitees(client: AsyncClient, organisation_id: str):
    data = {
        "page": 1,
        "perPage": 10,
        "email": "email@email.com",
        "sortBy": InvitationSortingField.EMAIL_ASC.value,
    }

    iam_url = f"{IAM_BASE_URL}/organisations/{organisation_id}/invitees?{urlencode(data)}"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=ORGANISATION_INVITEES_JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{organisation_id}/invitees",
            params=data,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == ORGANISATION_INVITEES_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_get_organisation_approvals(client: AsyncClient, organisation_id: str):
    data = {
        "page": 1,
        "perPage": 10,
        "fullName": "",
        "sortBy": UserSortingField.FULL_NAME_ASC.value,
    }

    iam_url = f"{IAM_BASE_URL}/organisations/{organisation_id}/approvals?{urlencode(data)}"

    with aioresponses() as mock_response:
        mock_response.get(iam_url, status=HTTPStatus.OK, body=ORGANISATION_USERS_JSON)

        response = await client.get(
            f"{BASE_API_V5_PREFIX}/iam/organisations/{organisation_id}/approvals",
            params=data,
        )

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == ORGANISATION_USERS_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_create_organisation(client: AsyncClient, organisation_id: str):
    iam_url = f"{IAM_BASE_URL}/organisations"

    with aioresponses() as mock_response:
        mock_response.post(iam_url, status=HTTPStatus.CREATED, body=ORGANISATION_JSON)

        response = await client.post(f"{BASE_API_V5_PREFIX}/iam/organisations", json=ORGANISATION_DICT)

        assert response.status_code == HTTPStatus.CREATED
        mock_response.assert_called_once()
        assert response.json() == ORGANISATION_DICT


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_delete_organisation(client: AsyncClient, organisation_id: str):
    iam_url = f"{IAM_BASE_URL}/organisations/{organisation_id}"

    with aioresponses() as mock_response:
        mock_response.delete(iam_url, status=HTTPStatus.OK)

        response = await client.delete(f"{BASE_API_V5_PREFIX}/iam/organisations/{organisation_id}")

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_response.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.iam_endpoints
async def test_update_organisation(client: AsyncClient, organisation_id: str):
    iam_url = f"{IAM_BASE_URL}/organisations/{organisation_id}"
    data = {
        "name": "name2",
        "customizationUrl": "customizationUrl2",
    }

    with aioresponses() as mock_response:
        mock_response.patch(iam_url, status=HTTPStatus.OK, body=ORGANISATION_JSON)

        response = await client.patch(f"{BASE_API_V5_PREFIX}/iam/organisations/{organisation_id}", json=data)

        assert response.status_code == HTTPStatus.OK
        mock_response.assert_called_once()
        assert response.json() == ORGANISATION_DICT
