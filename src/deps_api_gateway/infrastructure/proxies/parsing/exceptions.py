from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["ParsingProxyRequestError", "ParsingServiceUnavailableError"]


class ParsingProxyRequestError(BaseApiGatewayException):
    code = "parsing_error"


class ParsingServiceUnavailableError(ServiceUnavailableError):
    code = "parsing_service_unavailable_error"
