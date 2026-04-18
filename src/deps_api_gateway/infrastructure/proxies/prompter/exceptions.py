from deps_api_gateway.domain.exceptions import BaseApiGatewayException

__all__ = ["PrompterError"]


class PrompterError(BaseApiGatewayException):
    code = "prompter_error"
