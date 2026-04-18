from pydantic_settings import BaseSettings

__all__ = ["Settings"]


class Settings(BaseSettings):
    services: str = "[]"
