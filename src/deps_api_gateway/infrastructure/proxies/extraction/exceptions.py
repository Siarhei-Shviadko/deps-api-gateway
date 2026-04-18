from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["ExtractionError", "ExtractionServiceUnavailableError"]


class ExtractionError(BaseApiGatewayException):
    code = "extraction_error"


class ExtractionServiceUnavailableError(ServiceUnavailableError):
    code = "extraction_service_unavailable_error"
