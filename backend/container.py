from dependency_injector import providers, containers

from backend.config import settings
from backend.shared import LoggingLogger, FastApiRedisCache
from backend.auctions import AuctionsService, SQLAlchemyAuctionsRepository


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[settings])
    wiring_config = containers.WiringConfiguration(packages=[".auctions"])
    # General
    logging_logger = providers.Singleton(
        LoggingLogger,
        name=config.logger.NAME,
        filename=config.logger.FILENAME,
        filemode=config.logger.FILEMODE,
        level=config.logger.LEVEL,
        format_=config.logger.FORMAT,
        date_format=config.logger.DATE_FORMAT,
    )
    fastapi_redis_cache = providers.Singleton(
        FastApiRedisCache,
        url=config.cache.url,
    )

    # Auth

    # Auctions
    auctions_repository = providers.Singleton(
        SQLAlchemyAuctionsRepository, db_url=config.auctions.DB_URL
    )

    auctions_service = providers.Factory(
        AuctionsService,
        repository=auctions_repository,
        logger=logging_logger,
        cache=fastapi_redis_cache,
    )
