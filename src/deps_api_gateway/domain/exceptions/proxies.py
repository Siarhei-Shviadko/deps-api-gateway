from .base import BaseApiGatewayException

__all__ = [
    "WorkflowManagerError",
    "DocumentTypeError",
    "UnifiedDataError",
    "ExtractedDataError",
    "UploadDocumentError",
    "PipelineError",
    "DocumentError",
    "OCRError",
    "ExtractionError",
]


class DocumentTypeError(BaseApiGatewayException):
    code = "document_type_error"


class DocumentError(BaseApiGatewayException):
    code = "document_error"


class OCRError(BaseApiGatewayException):
    code = "ocr_error"


class WorkflowManagerError(BaseApiGatewayException):
    code = "workflow_manager_error"


class UnifiedDataError(BaseApiGatewayException):
    code = "unified_data_error"


class ExtractedDataError(BaseApiGatewayException):
    code = "extracted_data_error"


class UploadDocumentError(BaseApiGatewayException):
    code = "upload-document-error"


class PipelineError(BaseApiGatewayException):
    code = "run-pipeline-error"


class ExtractionError(BaseApiGatewayException):
    code = "extraction_error"
