"""
Centralized application configuration.

This is the ONLY settings module in the project. Earlier revisions had two
overlapping config systems (app/core/config.py + app/config/settings.py) —
that duplication has been removed. Every setting the app needs, from every
integration, lives here and nowhere else.
"""
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ------------------------------------------------------------------
    # App / general
    # ------------------------------------------------------------------
    APP_NAME: str = "AutoMateAI"
    ENVIRONMENT: str = "development"
    BASE_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    LOG_LEVEL: str = "INFO"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    # Defaults to a local SQLite file so the project runs with zero external
    # setup. Swap to a Postgres URL (e.g. postgresql+psycopg2://...) later —
    # every model/query here is plain SQLAlchemy, no code changes needed.
    DATABASE_URL: str = "sqlite:///./automateai.db"

    # ------------------------------------------------------------------
    # Auth / JWT
    # ------------------------------------------------------------------
    JWT_SECRET_KEY: str = Field(default="CHANGE_ME_IN_PRODUCTION_" + "x" * 32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    AUTH_COOKIE_NAME: str = "automateai_session"
    AUTH_COOKIE_SECURE: bool = False  # set True behind HTTPS in production

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------
    GROQ_API_KEY: Optional[str] = None
    MODEL_NAME: str = "llama-3.3-70b-versatile"

    # ------------------------------------------------------------------
    # Tool providers
    # ------------------------------------------------------------------
    OPENWEATHER_API_KEY: Optional[str] = None
    SERPAPI_API_KEY: Optional[str] = None
    GOOGLE_MAPS_API_KEY: Optional[str] = None

    # ------------------------------------------------------------------
    # Vapi (Voice AI)
    # ------------------------------------------------------------------
    VAPI_API_KEY: Optional[str] = None
    VAPI_BASE_URL: str = "https://api.vapi.ai"
    VAPI_ASSISTANT_ID: Optional[str] = None
    VAPI_PHONE_NUMBER_ID: Optional[str] = None
    VAPI_WEBHOOK_SECRET: Optional[str] = None

    # ------------------------------------------------------------------
    # Twilio
    # ------------------------------------------------------------------
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    TWILIO_VALIDATE_SIGNATURE: bool = True

    # ------------------------------------------------------------------
    # Google (Gmail / Calendar / Drive / Sheets) OAuth
    # ------------------------------------------------------------------
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/google/oauth/callback"
    GOOGLE_SCOPES: List[str] = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets",
    ]

    @field_validator("GOOGLE_SCOPES", mode="before")
    @classmethod
    def _split_scopes(cls, v):
        if isinstance(v, str):
            return v.split()
        return v

    # ------------------------------------------------------------------
    # n8n (generic automation webhook)
    # ------------------------------------------------------------------
    N8N_WEBHOOK_URL: Optional[str] = None
    N8N_WEBHOOK_TOKEN: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
