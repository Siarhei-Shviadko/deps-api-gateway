from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["HighSparrowError", "HighSparrowServiceUnavailableError"]


class HighSparrowError(BaseApiGatewayException):
    code = "high_sparrow_error"


class HighSparrowServiceUnavailableError(ServiceUnavailableError):
    code = "high_sparrow_service_unavailable_error"
