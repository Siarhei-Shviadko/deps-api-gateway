from enum import Enum


class ExtractionType(str, Enum):
    PLUGIN = "plugin"
    TEMPLATE = "template"
    PROTOTYPE = "prototype"
    NON = "non"

    def to_corleone(self) -> str:
        corleone_extraction_type = {
            "template": "template",
            "plugin": "ml",
            "prototype": "prototype",
        }
        return corleone_extraction_type[self.value]


class DocumentTypeSource(str, Enum):
    CORLEONE = "corleone"
    DOCUMENT_TYPE = "document_type"


class UnifiedDataSource(str, Enum):
    PREPROCESS = "preprocess"
    UNIFIER = "unifier"


class ExtractedDataSource(str, Enum):
    CORLEONE = "corleone"
    EXTRACTION = "extraction"


class ImportSource(str, Enum):
    GOOGLE_DRIVE = "GoogleDrive"


NULL_CONFIDENCE: float = -1.0

PLUGIN_EXTRACTION_TYPE = "plugin"
EXTRACTION_TYPE_PLACEHOLDER = "ET"
PROJECT_NAME = "api-gateway"
DESCRIPTION = ""
V1_PREFIX = "/v1"
V2_PREFIX = "/v2"
V5_PREFIX = "/v5"
BASE_API_PREFIX = "/api/api-gateway"
API_PREFIX = BASE_API_PREFIX + V1_PREFIX
API_V5_PREFIX = BASE_API_PREFIX + V5_PREFIX
BASE_API_V1_PREFIX = "/api/v1"
BASE_API_V5_PREFIX = "/api/v5"
BASE_API_V6_PREFIX = "/api/v6"
SWAGGER_DOC_URL = "/docs"

V5_DOCUMENT_CREATE_IMPORT_DEPRECATION_WARNING = (
    "This v5 endpoint is deprecated. Use the v6 API (/api/v6/documents) with mandatory documentType instead."
)

CORLEONE_BASE_API_PREFIX = "/api/corleone"
PREPROCESS_BASE_API_PREFIX = "/api/preprocess"
DOCUMENT_BASE_API_PREFIX = "/api/document"
DOCUMENT_TYPE_BASE_API_PREFIX = "/api/document-type"
UNIFIER_BASE_API_PREFIX = "/api/unifier"
EXTRACTION_BASE_API_PREFIX = "/api/extraction"
WORKFLOW_MANAGER_BASE_API_PREFIX = "/api/workflow-manager"
IAM_BASE_API_PREFIX = "/api/iam"
OCR_BASE_API_PREFIX = "/api/ocr"
PROTOTYPE_BASE_API_PREFIX = "/api/prototype"
PARSING_BASE_API_PREFIX = "/api/parsing"
ENRICHMENT_BASE_PREFIX = "/api/enrichment"
PROMPTER_BASE_PREFIX = "/api/prompter"
HIGH_SPARROW_BASE_PREFIX = "/api/high-sparrow"
OUTPUT_EXPORTING_BASE_PREFIX = "/api/output-exporting"
VALIDATION_BASE_PREFIX = "/api/validation"
AI_FUSION_BASE_PREFIX = "/api/ai-fusion"
TEMPLATE_BASE_API_PREFIX = "/api/template"
GROUPS_BASE_API_PREFIX = "/api/groups"
CLASSIFICATION_BASE_API_PREFIX = "/api/classification"
CLOUD_NATIVE_BASE_API_PREFIX = "/api/cloud-native-extraction"
STORAGE_BASE_API_PREFIX = "/api/storage"
FILES_BATCH_BASE_API_PREFIX = "/api/files-batch"
EVENT_RELAY_BASE_API_PREFIX = "/api/event-relay"
DOCUMENT_ROUTER_PREFIX = "/documents"
DOCUMENT_TYPE_ROUTER_PREFIX = "/document-types"
IAM_ROUTER_PREFIX = "/iam"
GROUPS_ROUTER_PREFIX = "/groups"
BATCH_ROUTER_PREFIX = "/batches"
EVENT_RELAY_ROUTER_PREFIX = "/event-relay"
AGENTIC_AI_ROUTER_PREFIX = "/agentic-ai"
AGENTIC_AI_BASE_API_PREFIX = "/api/agentic-ai"
FILES_BASE_API_PREFIX = "api/file"
FILES_ROUTER_PREFIX = "/files"
META_AGENT_BASE_API_PREFIX = "/api/meta-agent"
SEMANTIC_PARSING_BASE_API_PREFIX = "/api/semantic-parsing"

DEPS_TOKEN_HEADER_NAME = "deps-token"  # noqa: S105
JSON_CONTENT_TYPE = "application/json"

GENERIC_ERROR_MESSAGE = "Something went wrong. Please try again later."
SERVICE_CONNECTION_ERROR_MESSAGES = ("Cannot connect to host", "Connection refused", "Connection timed out")
