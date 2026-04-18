from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["UnifierError", "UnifierServiceUnavailableError"]


class UnifierError(BaseApiGatewayException):
    code = "unifier_error"


class UnifierServiceUnavailableError(ServiceUnavailableError):
    code = "unifier_service_unavailable_error"
