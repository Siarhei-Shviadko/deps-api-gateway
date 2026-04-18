from deps_api_gateway.domain.exceptions import ServiceUnavailableError

__all__ = ["MetaAgentServiceUnavailableError"]


class MetaAgentServiceUnavailableError(ServiceUnavailableError):
    code = "meta_agent_service_unavailable_error"
