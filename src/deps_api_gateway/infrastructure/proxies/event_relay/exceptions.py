from deps_api_gateway.domain.exceptions import BaseApiGatewayException

__all__ = ["EventRelayError"]


class EventRelayError(BaseApiGatewayException):
    code = "event_relay_error"
