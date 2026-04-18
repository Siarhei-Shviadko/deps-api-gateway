from deps_api_gateway.domain.exceptions import ServiceUnavailableError

__all__ = ["FileServiceUnavailableError"]


class FileServiceUnavailableError(ServiceUnavailableError):
    code = "file_service_unavailable_error"
