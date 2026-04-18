from deps_api_gateway.domain.exceptions import ServiceUnavailableError

__all__ = [
    "CloudNativeExtractionServiceUnavailableError",
]


class CloudNativeExtractionServiceUnavailableError(ServiceUnavailableError):
    code = "cloud_native_extraction_service_unavailable_error"
