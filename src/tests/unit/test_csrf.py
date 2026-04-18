from http import HTTPStatus

import pytest
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import InvalidHeaderError, TokenValidationError

from deps_api_gateway import csrf
from deps_api_gateway.domain.exceptions.csrf import CsrfValidationError


@pytest.fixture
def csrf_protect_mock(mocker, monkeypatch):
    mock_csrf = mocker.Mock(CsrfProtect)
    monkeypatch.setattr(
        csrf.CsrfProtect,
        "__new__",
        mocker.Mock(return_value=mock_csrf),
    )
    yield mock_csrf


@pytest.mark.asyncio
async def test_validate_csrf_token__valid_token_in_headers__no_error_is_raised(csrf_protect_mock, mocker):
    await csrf.validate_csrf_token(mocker.Mock())

    csrf_protect_mock.validate_csrf.assert_called_once()


@pytest.mark.asyncio
async def test_validate_csrf_token__no_token_in_header__csrf_validation_error_is_raised(csrf_protect_mock, mocker):
    csrf_protect_mock.validate_csrf.side_effect = InvalidHeaderError("test")

    with pytest.raises(CsrfValidationError) as err_info:
        await csrf.validate_csrf_token(mocker.Mock())

    assert err_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert str(err_info.value) == "test"


@pytest.mark.asyncio
async def test_validate_csrf_token__failed_to_validate_token__csrf_validation_error_is_raised(
    csrf_protect_mock, mocker
):
    csrf_protect_mock.validate_csrf.side_effect = TokenValidationError("test")

    with pytest.raises(CsrfValidationError) as err_info:
        await csrf.validate_csrf_token(mocker.Mock())

    assert err_info.value.status_code == HTTPStatus.UNAUTHORIZED
    assert str(err_info.value) == "test"
