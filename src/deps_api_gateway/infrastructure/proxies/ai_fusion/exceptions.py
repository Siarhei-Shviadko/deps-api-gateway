from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["AIFusionError", "AIFusionServiceUnavailableError"]


class AIFusionError(BaseApiGatewayException):
    code = "ai_fusion_error"


class AIFusionServiceUnavailableError(ServiceUnavailableError):
    code = "ai_fusion_service_unavailable_error"
