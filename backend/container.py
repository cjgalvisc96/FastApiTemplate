from dependency_injector import providers, containers

from backend.config import settings
from backend.shared import SQLAlchemyDatabase, FastApiRedisCacheImp
from backend.users import AuthService, UsersService, SQLAlchemyUsersRepositoryImp


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[settings])
    wiring_config = containers.WiringConfiguration(packages=[".users"])

    # General
    fastapi_redis_cache = providers.Singleton(
        FastApiRedisCacheImp,
        url=config.cache.url,
    )
    db = providers.Singleton(
        SQLAlchemyDatabase,
        db_url=config.db.DB_URL,
    )

    # Users
    users_repository = providers.Factory(
        SQLAlchemyUsersRepositoryImp, session_factory=db.provided.session
    )
    users_service = providers.Factory(UsersService, repository=users_repository)

    # Auth
    auth_service = providers.Factory(
        AuthService,
        secret_key=config.users.SECRET_KEY,
        algorithm=config.users.ALGORITHM,
        default_token_time_expiration=config.users.ACCESS_TOKEN_EXPIRE_MINUTES,
        get_user_by_filter=users_repository.provided.get_by_filter,
    )
