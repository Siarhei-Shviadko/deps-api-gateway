from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["IAMError", "IAMServiceUnavailableError"]


class IAMError(BaseApiGatewayException):
    code = "iam_error"


class IAMServiceUnavailableError(ServiceUnavailableError):
    code = "iam_service_unavailable_error"
