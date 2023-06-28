from logging import INFO
from functools import lru_cache

from pydantic import Field, BaseSettings

ENV_FILE = "dev.env"
CASE_SENSITIVE = True


class FastApiRedisCacheImpSettings(BaseSettings):
    url: str = Field(env="CACHE_URL")

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class DBSettings(BaseSettings):
    DB_URL: str
    TEST_DB_URL: str

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str
    result_backend: str = Field(env="CELERY_RESULT_BACKEND")
    imports: list[str] = [
        "backend.users.tasks",
    ]
    CELERY_BROKER_TRANSPORT: str = "sqs"
    result_expires: int = 60 * 60 * 24  # 1 day

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class LoggerSettings(BaseSettings):
    NAME: str = "BackendLogger"
    FILENAME: str = "logs.txt"
    FILEMODE: str = "a"
    LEVEL: int = INFO
    FORMAT: str = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    DATE_FORMAT: str = "%d-%b-%y %H:%M:%S"


class UsersSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


class Settings(BaseSettings):
    logger = LoggerSettings()
    db = DBSettings()
    users = UsersSettings()
    celery = CelerySettings()
    cache = FastApiRedisCacheImpSettings()

    class Config:
        case_sensitive = CASE_SENSITIVE
        env_file = ENV_FILE


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
