from logging import INFO
from functools import lru_cache

from pydantic import BaseSettings

ENV_FILE = "dev.env"
CASE_SENSITIVE = True


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
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


class Settings(BaseSettings):
    logger = LoggerSettings()
    auctions = AuctionsSettings()
    celery = CelerySettings()

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
