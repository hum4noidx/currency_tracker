import logging
from typing import Optional, List

from pydantic import PostgresDsn, field_validator, AnyHttpUrl
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Image Process Service"
    API_PATH: str = "/api/v1"
    DATABASE_URL: PostgresDsn
    ASYNC_DATABASE_URL: Optional[PostgresDsn] = None
    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = []

    @field_validator("ASYNC_DATABASE_URL")
    def build_async_database_url(cls, v: Optional[str], info: FieldValidationInfo):
        """Builds ASYNC_DATABASE_URL from DATABASE_URL."""
        url: MultiHostUrl | str = info.data.get("DATABASE_URL")
        url = str(url)
        return url.replace("postgresql", "postgresql+asyncpg", 1)

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
