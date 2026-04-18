from deps_api_gateway.domain.exceptions import BaseApiGatewayException

__all__ = ["ExtractorAttachmentError"]


class ExtractorAttachmentError(BaseApiGatewayException):
    code = "extractor_attachment_error"
