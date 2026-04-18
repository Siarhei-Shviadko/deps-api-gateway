from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = [
    "GroupsError",
    "GroupsServiceUnavailableError",
]


class GroupsError(BaseApiGatewayException):
    code = "groups_error"


class GroupsServiceUnavailableError(ServiceUnavailableError):
    code = "groups_service_unavailable_error"
