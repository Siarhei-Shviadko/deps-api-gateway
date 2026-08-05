from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = [
    "SplittingError",
    "SplittingServiceUnavailableError",
]


class SplittingError(BaseApiGatewayException):
    code = "splitting_error"


class SplittingServiceUnavailableError(ServiceUnavailableError):
    code = "splitting_service_unavailable_error"
