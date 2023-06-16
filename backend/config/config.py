from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    EXTERNAL_PROVIDER_API_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
