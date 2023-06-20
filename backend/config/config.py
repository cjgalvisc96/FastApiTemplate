from logging import INFO
from functools import lru_cache

from pydantic import BaseSettings

ENV_FILE = "dev.env"
CASE_SENSITIVE = True


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

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
