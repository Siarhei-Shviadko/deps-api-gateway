from deps_api_gateway.domain.exceptions import ServiceUnavailableError

__all__ = ["ClassificationServiceUnavailableError"]


class ClassificationServiceUnavailableError(ServiceUnavailableError):
    code = "classification_service_unavailable_error"
