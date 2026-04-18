from deps_api_gateway.domain.exceptions import ServiceUnavailableError

__all__ = ["DocumentsServiceUnavailableError"]


class DocumentsServiceUnavailableError(ServiceUnavailableError):
    code = "documents_service_unavailable_error"
