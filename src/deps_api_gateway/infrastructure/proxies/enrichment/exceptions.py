from deps_api_gateway.domain.exceptions import (
    BaseApiGatewayException,
    ForbiddenError,
    NotFoundError,
    ServiceUnavailableError,
)

__all__ = [
    "EnrichmentError",
    "EnrichmentForbiddenError",
    "DocumentTypeNotFound",
    "SupplementNotFound",
    "EnrichmentServiceUnavailableError",
]


class EnrichmentError(BaseApiGatewayException):
    code = "enrichment_error"


class EnrichmentForbiddenError(ForbiddenError):
    code = "enrichment_forbidden_error"


class DocumentTypeNotFound(NotFoundError):
    code = "document_type_not_found"


class SupplementNotFound(NotFoundError):
    code = "supplement_not_found_error"

    def __init__(self, supplement_id: str) -> None:
        super().__init__(
            f"Supplement with id `{supplement_id}` not found",
        )


class EnrichmentServiceUnavailableError(ServiceUnavailableError):
    code = "enrichment_service_unavailable_error"
