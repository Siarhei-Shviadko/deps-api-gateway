from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ServiceUnavailableError,
)

__all__ = ["OCRError", "OCRServiceUnavailableError"]


class OCRError(BaseApiGatewayException):
    code = "ocr_error"


class OCRServiceUnavailableError(ServiceUnavailableError):
    code = "ocr_service_unavailable_error"
