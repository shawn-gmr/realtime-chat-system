from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHAT_", extra="ignore")

    app_name: str = "Real-Time Chat System"
    database_url: str = Field(default="sqlite+aiosqlite:///./chat-system.db")
    heartbeat_timeout_seconds: int = Field(default=30)
    away_timeout_minutes: int = Field(default=5)
    applicationinsights_connection_string: str | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
