from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # --- Application ---
    app_name: str = "AI Personal Financial Coach"
    app_env: str = "development"
    debug: bool = True
    api_version: str = "v1"

    # --- Google Gemini ---
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite-preview"

    # --- Database ---
    database_url: str = "sqlite+aiosqlite:///./data/financial_coach.db"

    # --- Dashboard ---
    dashboard_port: int = 8501

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
