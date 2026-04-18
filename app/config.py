from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    app_env: str = getenv("APP_ENV", "development")
    log_level: str = getenv("LOG_LEVEL", "INFO")
    database_url: str = getenv("DATABASE_URL", "sqlite:///./ar_analyst.db")
    anthropic_api_key: str | None = getenv("ANTHROPIC_API_KEY")


settings = Settings()