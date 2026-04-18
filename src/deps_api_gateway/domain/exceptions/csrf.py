import http

from .base import BaseApiGatewayException

__all__ = ["CsrfValidationError"]


class CsrfValidationError(BaseApiGatewayException):
    code = "csrf_validation_error"

    def __init__(self, detail: str, status_code: int = http.HTTPStatus.UNAUTHORIZED):
        super().__init__(detail)
        self.status_code = status_code
