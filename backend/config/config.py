from logging import INFO
from functools import lru_cache

from pydantic import Field, BaseSettings

ENV_FILE = "dev.env"
CASE_SENSITIVE = True


class FastApiRedisCacheSettings(BaseSettings):
    url: str = Field(env="CACHE_URL")

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str
    result_backend: str = Field(env="CELERY_RESULT_BACKEND")
    imports: list[str] = [
        "backend.auctions.tasks",
    ]
    CELERY_BROKER_TRANSPORT: str = "sqs"
    result_expires: int = 60 * 60 * 24  # 1 day

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class LoggerSettings(BaseSettings):
    NAME: str = "BackendLogger"
    FILENMAE: str = "logs.txt"
    FILEMODE: str = "a"
    LEVEL: int = INFO
    FORMAT: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    DATE_FORMAT: str = "%d-%b-%y %H:%M:%S"


class AuctionsSettings(BaseSettings):
    DB_URL: str

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class UsersSettings(BaseSettings):
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class Settings(BaseSettings):
    logger = LoggerSettings()
    auctions = AuctionsSettings()
    users = UsersSettings()
    celery = CelerySettings()
    cache = FastApiRedisCacheSettings()

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
