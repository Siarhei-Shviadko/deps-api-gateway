import json
from unittest.mock import patch

import pytest
from fastapi import Request

from deps_api_gateway.api import set_user_from_token


@pytest.mark.parametrize(
    "url",
    (
        "/api/api-gateway/debug/500",
        "/api/api-gateway/healthcheck",
        "/api/api-gateway/v1/service-info/version",
        "/api/api-gateway/v1/docs",
        "/api/api-gateway/v1/openapi.json",
        "/favicon.ico",
        "/api/document/v1/debug/500",
        "/api/document/healthcheck",
        "/api/document/v1/service-info/version",
        "/api/document/docs",
    ),
)
@patch("deps_api_gateway.api.auth.user")
def test_set_deps_token__public_endpoints__not_set(mocked_user, mocker, url):
    request = mocker.Mock(Request)
    request.url.path = url

    set_user_from_token(request)

    mocked_user.set.assert_not_called()


@patch("deps_api_gateway.api.auth.user")
def test_set_deps_token__private_endpoints__set(mocked_user, mocker, tenant_id):
    deps_token = {"organisation": tenant_id}
    expected_deps_token = {"organisation": tenant_id, "deps_token": json.dumps(deps_token)}
    request = mocker.Mock(Request)
    request.url.path = "api/document/v1/documents"
    request.headers = {"deps-token": json.dumps(deps_token)}

    set_user_from_token(request)

    mocked_user.set.assert_called_once_with(expected_deps_token)
