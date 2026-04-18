from fastapi.requests import Request
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from deps_api_gateway.domain.exceptions.csrf import CsrfValidationError
from deps_api_gateway.settings import CSRFSettings


@CsrfProtect.load_config
def get_csrf_config() -> CSRFSettings:
    return CSRFSettings()


async def validate_csrf_token(request: Request) -> None:
    csrf_protect = CsrfProtect()
    try:
        await csrf_protect.validate_csrf(request)
    except CsrfProtectError as err:
        raise CsrfValidationError(err.message, err.status_code)
