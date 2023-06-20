from logging import INFO

from dependency_injector import providers, containers

from backend.shared import LoggingLogger
from backend.auctions import CreateAuctionService, SQLAlchemyAuctionsRepository


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(json_files=["container_config.json"])
    wiring_config = containers.WiringConfiguration(packages=[".auctions"])
    # General
    logger = providers.Singleton(
        LoggingLogger,
        name=config.logger.name,
        filename=config.logger.filename,
        filemode=config.logger.filemode,
        level=INFO,
        format_=config.logger.format_,
        date_format=config.logger.date_format,
    )

    # Auctions
    auctions_repository = providers.Singleton(
        SQLAlchemyAuctionsRepository, db_url=config.auctions_repository.db_url
    )

    create_auction_service = providers.Factory(
        CreateAuctionService, repository=auctions_repository, logger=logger
    )
