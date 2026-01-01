from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_CONNECTION_STRING: str
    JWT_ALGORITHM: str | None = None
    JWT_SECRET_KEY: str | None = None
    JWT_ACCESS_COOKIE_NAME: str | None = None
    JWT_TOKEN_LOCATION: list[str] | None = None

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8"
    )

settings = Settings()