from functools import lru_cache
from typing import Optional, Dict, Any

from pydantic import validator, PostgresDsn
from pydantic_settings import BaseSettings
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
import logging

config = Config(".env")


class APPSettings(BaseSettings):
    PROJECT_NAME: str = config("PROJECT_NAME", cast=str, default="TemplateService")
    VERSION: str = config("VERSION", cast=str, default="1.0.0")

    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    ENV: str = config("ENV", cast=str, default="TEST")

    POSTGRES_SERVER: str = config("POSTGRES_SERVER", cast=str, default="127.0.0.1")
    POSTGRES_PORT: str = config("POSTGRES_PORT", cast=int, default=5432)
    POSTGRES_USER: str = config("POSTGRES_USER", cast=str, default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str, default="postgres")
    POSTGRES_DB: str = config("POSTGRES_DB", cast=str, default="postgres")

    SQL_DEBUG: bool = config("SQL_DEBUG", cast=bool, default=False)

    API_ROUTE: str = config("API_ROUTE", cast=str, default="/path")
    API_ROOT_PATH: str = config("API_ROOT_PATH", default="")

    LOGGING_LEVEL: str = config("LOGGING_LEVEL", cast=str, default="INFO")
    LOGGING_SERIALIZE: bool = config("LOGGING_SERIALIZE", cast=bool, default=False)

    HTTP_CLIENT_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_MAX_ATTEMPTS", cast=int, default=3
    )
    HTTP_CLIENT_START_TIMEOUT: float = config(
        "HTTP_CLIENT_START_TIMEOUT", cast=float, default=0.1
    )
    HTTP_CLIENT_MAX_TIMEOUT: float = config(
        "HTTP_CLIENT_MAX_TIMEOUT", cast=float, default=30.0
    )
    HTTP_CLIENT_BACKOFF_FACTOR: float = config(
        "HTTP_CLIENT_BACKOFF_FACTOR", cast=float, default=2.0
    )
    HTTP_CLIENT_DNS_MAX_ATTEMPTS: int = config(
        "HTTP_CLIENT_DNS_MAX_ATTEMPTS", cast=int, default=4
    )
    HTTP_CLIENT_DNS_TIMEOUT: float = config(
        "HTTP_CLIENT_DNS_TIMEOUT", cast=float, default=5.0
    )
    HTTP_CLIENT_RAISE_FOR_STATUS: bool = config(
        "HTTP_CLIENT_RAISE_FOR_STATUS", cast=bool, default=False
    )
    HTTP_CLIENT_RETRY_STATUSES: Optional[CommaSeparatedStrings] = config(
        "HTTP_CLIENT_RETRY_STATUSES", cast=CommaSeparatedStrings, default=None
    )
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=1)
    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)

    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        url = PostgresDsn.build(
            scheme="postgres",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=int(values.get("POSTGRES_PORT")),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )
        return url.unicode_string()

    class Config:
        env_file = ".env"


@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
