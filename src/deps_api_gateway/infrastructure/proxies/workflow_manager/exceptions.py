from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["WorkflowManagerError", "WorkflowManagerServiceUnavailableError"]


class WorkflowManagerError(BaseApiGatewayException):
    code = "workflow_manager_error"


class WorkflowManagerServiceUnavailableError(ServiceUnavailableError):
    code = "workflow_manager_service_unavailable_error"
