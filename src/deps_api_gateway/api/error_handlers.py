import logging
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request

from deps_api_gateway.constants import GENERIC_ERROR_MESSAGE
from deps_api_gateway.domain.exceptions import (
    AuthorizationError,
    BaseApiGatewayException,
    ForbiddenError,
    IllegalArgument,
    NotFoundError,
    ServiceUnavailableError,
)

from .serializers import ErrorModel
from .utilities import handle_connection_error, is_connection_error

logger = logging.getLogger(__name__)


def json_api_gateway_exception_error_handler(error: BaseApiGatewayException, status_code: int) -> JSONResponse:
    if is_connection_error(error):
        return handle_connection_error(error)

    return JSONResponse(
        status_code=status_code,
        content=ErrorModel(code=error.code, message=str(error)).model_dump(),
    )  # noqa: WPS221


def register_error_handler(app: FastAPI) -> None:
    @app.exception_handler(ServiceUnavailableError)
    def handle_service_unavailable_error(req: Request, error: ServiceUnavailableError) -> JSONResponse:  # noqa: WPS430
        return JSONResponse(
            status_code=HTTPStatus.BAD_GATEWAY,
            content=ErrorModel(code=error.code, message=error.code).model_dump(),
        )

    @app.exception_handler(BaseApiGatewayException)
    def handle_api_gateway_exception(req: Request, error: BaseApiGatewayException) -> JSONResponse:  # noqa: WPS430
        logger.error(f"API Gateway exception {error.__class__.__name__} occurred: '{error}'", exc_info=True)

        mapper = [
            (AuthorizationError, HTTPStatus.UNAUTHORIZED),
            (NotFoundError, HTTPStatus.NOT_FOUND),
            (ForbiddenError, HTTPStatus.FORBIDDEN),
            (IllegalArgument, HTTPStatus.UNPROCESSABLE_ENTITY),
            (BaseApiGatewayException, HTTPStatus.BAD_REQUEST),
        ]

        for error_type, status_code in mapper:
            if issubclass(type(error), error_type):
                return json_api_gateway_exception_error_handler(error, status_code)

    @app.exception_handler(ValidationError)
    def bad_request(req: Request, exc: ValidationError) -> JSONResponse:  # noqa: WPS430
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=ErrorModel(code="bad_request", message=str(exc)).model_dump(),
        )

    @app.exception_handler(Exception)
    def handle_all_errors(req: Request, error: Exception) -> JSONResponse:  # noqa: WPS430
        logger.error(f"Unhandled error {error}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorModel(code="unhandled_error", message=GENERIC_ERROR_MESSAGE).model_dump(),
        )
