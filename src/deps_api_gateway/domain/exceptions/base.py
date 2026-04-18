from async_rest_client.exceptions import AsyncRestClientError

__all__ = [
    "BaseApiGatewayException",
    "IllegalArgument",
    "NotFoundError",
    "CompleteReviewError",
    "ForbiddenError",
    "ServiceUnavailableError",
]


class BaseApiGatewayException(Exception):
    code = "api_gateway_exception"


class IllegalArgument(BaseApiGatewayException):
    code = "illegal_argument"


class NotFoundError(BaseApiGatewayException):
    code = "not_found_error"


class CompleteReviewError(BaseApiGatewayException):
    code = "complete-review-error"


class ForbiddenError(BaseApiGatewayException):
    code = "forbidden_error"


class ServiceUnavailableError(BaseApiGatewayException, AsyncRestClientError):
    code = "service_unavailable_error"
