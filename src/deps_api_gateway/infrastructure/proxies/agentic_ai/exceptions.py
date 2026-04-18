from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["AgenticAIError", "AgenticAIServiceUnavailableError"]


class AgenticAIError(BaseApiGatewayException):
    code = "agentic_ai_error"


class AgenticAIServiceUnavailableError(ServiceUnavailableError):
    code = "agentic_ai_service_unavailable_error"
