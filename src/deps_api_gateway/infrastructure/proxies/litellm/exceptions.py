from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["LiteLLMError", "LiteLLMServiceUnavailableError"]


class LiteLLMError(BaseApiGatewayException):
    code = "litellm_error"


class LiteLLMServiceUnavailableError(ServiceUnavailableError):
    code = "litellm_service_unavailable_error"
