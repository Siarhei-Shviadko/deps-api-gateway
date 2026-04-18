from enum import Enum

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["SSLSettings", "DatabaseSettings", "ServiceInfoSettings", "AuthenticationSettings"]


class DBDialect(Enum):
    POSTGRES = "postgresql"
    MSSQL = "mssql"


class DBDriver(Enum):
    PSYCOPG2 = "psycopg2"
    PG8000 = "pg8000"
    PYTDS = "pytds"
    PYODBC = "pyodbc"


class SSLSettings(BaseSettings):
    key: str = ""
    cert: str = ""
    rootcert: str = ""
    mode: str = "verify-full"

    model_config = SettingsConfigDict(env_prefix="DATABASE_SSL")


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db: str
    ssl: SSLSettings = SSLSettings()
    dialect: DBDialect = DBDialect.POSTGRES
    driver: DBDriver = DBDriver.PSYCOPG2
    require_secure_transport: bool = False

    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class ServiceInfoSettings(BaseSettings):
    tag: str = ""
    date: str = ""
    hash: str = ""

    model_config = SettingsConfigDict(env_prefix="SERVICE_INFO_")


class AuthenticationSettings(BaseSettings):
    enabled: bool = Field(False, validation_alias="AUTH_ENABLED")
    verify_ssl: bool = Field(True, validation_alias="AUTH_VERIFY_SSL")
    certs_endpoint: str | None = Field(None, validation_alias="AUTH_CERTS_ENDPOINT")
    encryption_algorithm: str = Field("RS256", validation_alias="AUTH_ENCRYPTION_ALGORITHM")
    api_key: str | None = Field(None, validation_alias="API_KEY")

    @model_validator(mode="after")
    def validate_certs_endpoint_and_key(self):
        if self.enabled and (self.certs_endpoint is None and self.api_key is None):
            raise ValueError(
                "Please provide OAUTH certificates endpoint via `AUTH_CERTS_ENDPOINT` or provide auth key via `API_KEY`"
            )
        return self
