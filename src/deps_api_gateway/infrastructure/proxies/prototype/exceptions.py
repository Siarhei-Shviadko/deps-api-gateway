from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["PrototypeError", "PrototypeServiceUnavailableError"]


class PrototypeError(BaseApiGatewayException):
    code = "prototype_error"


class PrototypeServiceUnavailableError(ServiceUnavailableError):
    code = "prototype_service_unavailable_error"
