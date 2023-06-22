from dependency_injector import providers, containers

from backend.config import settings
from backend.shared import FastApiRedisCacheImp
from backend.auctions import AuctionsService, SQLAlchemyAuctionsRepositoryImp
from backend.users import AuthService, UsersService, SQLAlchemyUsersRepositoryImp


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[settings])
    wiring_config = containers.WiringConfiguration(packages=[".auctions", ".users"])
    # General
    fastapi_redis_cache = providers.Singleton(
        FastApiRedisCacheImp,
        url=config.cache.url,
    )
    # Users
    users_repository = providers.Singleton(SQLAlchemyUsersRepositoryImp, db_url=config.users.DB_URL)
    auth_service = providers.Singleton(
        AuthService,
        secret_key=config.users.SECRET_KEY,
        algorithm=config.users.ALGORITHM,
        default_token_time_expiration=config.users.ACCESS_TOKEN_EXPIRE_MINUTES,
        users_repository=users_repository,
    )
    users_service = providers.Factory(UsersService, repository=users_repository)

    # Auctions
    auctions_repository = providers.Singleton(
        SQLAlchemyAuctionsRepositoryImp, db_url=config.auctions.DB_URL
    )

    auctions_service = providers.Factory(
        AuctionsService,
        repository=auctions_repository,
        cache=fastapi_redis_cache,
    )
