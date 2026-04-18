from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["OutputExportingError", "OutputExportingServiceUnavailableError"]


class OutputExportingError(BaseApiGatewayException):
    code = "output_exporting_error"


class OutputExportingServiceUnavailableError(ServiceUnavailableError):
    code = "output_exporting_service_unavailable_error"
