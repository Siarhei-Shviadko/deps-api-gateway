from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["StorageError", "StorageServiceUnavailableError"]


class StorageError(BaseApiGatewayException):
    code = "storage_error"


class StorageServiceUnavailableError(ServiceUnavailableError):
    code = "storage_service_unavailable_error"
