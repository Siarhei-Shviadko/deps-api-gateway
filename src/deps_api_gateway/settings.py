from functools import lru_cache
from typing import Optional, Set

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from deps_api_gateway.extras.settings import AuthenticationSettings, ServiceInfoSettings


class CacheSettings(BaseSettings):
    document_type_source_cache_ttl: int = 900
    document_type_source_cache_max_size: int = 300
    document_type_code_cache_ttl: int = 900
    document_type_code_cache_max_size: int = 300
    rarely_updatable_cache_ttl: int = 3600
    rarely_updatable_cache_max_size: int = 30


class CSRFSettings(BaseSettings):
    secret_key: str = Field(default="", validation_alias="SECRET_KEY")
    max_age: int = 3600
    methods: Set[str] = {"POST", "PUT", "PATCH", "DELETE"}
    enabled: bool = Field(default=False, validation_alias="CSRF_PROTECTION_ENABLED")

    model_config = SettingsConfigDict(env_prefix="csrf_", case_sensitive=False)


class StorageSettings(BaseSettings):
    url: Optional[str] = Field(default=None, validation_alias="STORAGE_URL")
    default_storage: str = "FILE_STORAGE"


class Settings(BaseSettings):
    env: str = "development"
    version: str = "1.0"

    logger_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    authentication: AuthenticationSettings = AuthenticationSettings()
    info: ServiceInfoSettings = ServiceInfoSettings()
    csrf: CSRFSettings = CSRFSettings()
    storage: StorageSettings = StorageSettings()

    documentation_enabled: bool = True

    corleone_url: str
    preprocess_url: str
    document_url: str
    document_type_url: str
    unifier_url: str
    extraction_url: str
    workflow_manager_url: str
    iam_url: str
    ocr_url: str
    prototype_url: str
    parsing_url: str
    enrichment_url: str
    prompter_url: str
    high_sparrow_url: str
    output_exporting_url: str
    validation_url: str
    ai_fusion_url: str
    template_url: str
    groups_url: str
    classification_url: str
    cloud_native_extraction_url: str
    files_batch_url: str
    event_relay_url: str
    agentic_ai_url: str
    file_url: str
    meta_agent_url: str
    semantic_parsing_url: str

    cache_settings: CacheSettings = CacheSettings()

    authorization_enabled: bool = Field(False, validation_alias="AUTHORIZATION_ENABLED")  # noqa: WPS425

    workflow_v2: bool = False

    instrumentation_enabled: bool = False


@lru_cache()
def get_storage_settings() -> StorageSettings:
    return StorageSettings()
