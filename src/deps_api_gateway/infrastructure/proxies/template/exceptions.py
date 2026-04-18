from deps_api_gateway.domain.exceptions import ServiceUnavailableError

__all__ = ["TemplateServiceUnavailableError"]


class TemplateServiceUnavailableError(ServiceUnavailableError):
    code = "template_service_unavailable_error"
