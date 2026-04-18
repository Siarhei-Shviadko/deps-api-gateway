from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["DocumentTypeError", "DocumentTypeServiceUnavailableError"]


class DocumentTypeError(BaseApiGatewayException):
    code = "document_type_error"


class DocumentTypeServiceUnavailableError(ServiceUnavailableError):
    code = "document_type_service_unavailable_error"
