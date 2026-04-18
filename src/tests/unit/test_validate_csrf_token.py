from http import HTTPStatus

import pytest
from fastapi_csrf_protect import CsrfProtect

from deps_api_gateway import csrf
from deps_api_gateway.domain.exceptions.csrf import CsrfValidationError


@pytest.mark.asyncio
async def test_validate_csrf_token__valid_token_in_headers__no_error_is_raised(mocker):
    token, signed_token = CsrfProtect().generate_csrf_tokens(secret_key="")
    req_mock = mocker.Mock(spec=["headers", "cookies"])
    req_mock.headers = {"X-CSRF-Token": token}
    req_mock.cookies = {"fastapi-csrf-token": signed_token}
    await csrf.validate_csrf_token(req_mock)


@pytest.mark.asyncio
async def test_validate_csrf_token__no_token_in_header__csrf_validation_error_is_raised(mocker):
    req_mock = mocker.Mock()
    req_mock.headers = {}

    with pytest.raises(CsrfValidationError) as err_info:
        await csrf.validate_csrf_token(req_mock)

    assert err_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_validate_csrf_token__failed_to_validate_token__csrf_validation_error_is_raised(mocker):
    req_mock = mocker.Mock(spec=["headers", "cookies"])
    req_mock.headers = {"X-CSRF-Token": "test"}
    req_mock.cookies = {"fastapi-csrf-token": "test"}

    with pytest.raises(CsrfValidationError) as err_info:
        await csrf.validate_csrf_token(req_mock)

    assert err_info.value.status_code == HTTPStatus.UNAUTHORIZED
