from http import HTTPStatus

from fastapi.responses import JSONResponse

from deps_api_gateway.constants import SERVICE_CONNECTION_ERROR_MESSAGES
from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

from ..serializers import ErrorModel

__all__ = ["is_connection_error", "handle_connection_error"]


def is_connection_error(error: BaseApiGatewayException) -> bool:
    return any(error_message in str(error) for error_message in SERVICE_CONNECTION_ERROR_MESSAGES)


def generate_service_unavailable_error_code(error: BaseApiGatewayException) -> str:
    if hasattr(error, "code"):
        service_name = error.code.split("_error")[0]
        return f"{service_name}_service_unavailable_error"
    return ServiceUnavailableError().code


def handle_connection_error(error: BaseApiGatewayException) -> JSONResponse:
    error_code = generate_service_unavailable_error_code(error)
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content=ErrorModel(code=error_code, message=error_code).model_dump(),
    )
