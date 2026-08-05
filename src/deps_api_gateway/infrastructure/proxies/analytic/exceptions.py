from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = [
    "AnalyticError",
    "AnalyticServiceUnavailableError",
]


class AnalyticError(BaseApiGatewayException):
    code = "analytic_error"


class AnalyticServiceUnavailableError(ServiceUnavailableError):
    code = "analytic_service_unavailable_error"
