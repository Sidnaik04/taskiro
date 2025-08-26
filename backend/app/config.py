from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    gemini_api_key: str | None = None
    database_url: str | None = None
    cloudinary_url: str | None = None
    allowed_origins: List[AnyHttpUrl | str] = []

    class Config:
        env_file = "env"
        env_prefix = ""
        case_sensitive = False


settings = Settings()
