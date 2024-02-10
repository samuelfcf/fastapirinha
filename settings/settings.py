
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding='utf-8'
    )

    DATABASE_URL: str = "postgresql://app_user:app_password@localhost:5432/app_db"