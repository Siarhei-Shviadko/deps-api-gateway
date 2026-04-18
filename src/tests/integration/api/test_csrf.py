from http import HTTPStatus

import pytest

from deps_api_gateway import constants


class TestCSRFToken:
    endpoint = constants.BASE_API_V5_PREFIX

    @pytest.mark.asyncio
    async def test_get_csrf_token__returns_200(self, client):
        resp = await client.get(f"{self.endpoint}/csrf")

        assert resp.status_code == HTTPStatus.OK
        assert resp.json()["token"]
