from dependency_injector import providers, containers

from backend.config import settings
from backend.shared import LoggingLogger
from backend.auctions import CreateAuctionService, SQLAlchemyAuctionsRepository


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[settings])
    wiring_config = containers.WiringConfiguration(packages=[".auctions"])
    # General
    logger = providers.Singleton(
        LoggingLogger,
        name=config.logger.NAME,
        filename=config.logger.FILENAME,
        filemode=config.logger.FILEMODE,
        level=config.logger.LEVEL,
        format_=config.logger.FORMAT,
        date_format=config.logger.DATE_FORMAT,
    )

    # Auctions
    auctions_repository = providers.Singleton(
        SQLAlchemyAuctionsRepository, db_url=config.auctions.DB_URL
    )

    create_auction_service = providers.Factory(
        CreateAuctionService, repository=auctions_repository, logger=logger
    )
