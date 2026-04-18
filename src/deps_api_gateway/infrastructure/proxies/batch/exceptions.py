from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = [
    "BatchError",
    "BatchServiceUnavailableError",
]


class BatchError(BaseApiGatewayException):
    code = "batch_error"


class BatchServiceUnavailableError(ServiceUnavailableError):
    code = "batch_service_unavailable_error"
