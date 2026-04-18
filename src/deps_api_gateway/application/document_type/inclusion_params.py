from enum import Enum

__all__ = ["DocumentTypeExtras"]


class DocumentTypeExtras(str, Enum):
    EXTRACTION_FIELDS = "extraction-fields"
    EXTRA_FIELDS = "extra-fields"
    VALIDATORS = "validators"
    PROFILES = "profiles"
    CLASSIFIERS = "classifiers"
    LLM_EXTRACTORS = "llm-extractors"
    WORKFLOW_CONFIGURATIONS = "workflow-configurations"
