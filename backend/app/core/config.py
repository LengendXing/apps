from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:////home/myprojects/apps/data/ap_app.db"

    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 50
    FILE_EXPIRE_HOURS: int = 24
    ENABLE_BACKUP: bool = False
    BACKUP_INTERVAL_HOURS: int = 24

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
