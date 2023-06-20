from logging import INFO

from dependency_injector import providers, containers

from backend.shared import LoggingLogger
from backend.auctions import AuctionsRepository, CreateAuctionService


class ApplicationContainer(containers.DeclarativeContainer):
    # config = providers.Configuration(json_files=["./container_config.json"])
    wiring_config = containers.WiringConfiguration(packages=[".auctions"])
    # General
    # logger = providers.Singleton(
    #     LoggingLogger,
    #     name=config.logger.name(),
    #     filename=config.logger.filename(),
    #     filemode=config.logger.filemode(),
    #     level=INFO,
    #     format_=config.logger.format_(),
    #     date_format=config.logger.date_format(),
    # )

    logger = providers.Singleton(
        LoggingLogger,
        name="BackendLogger",
        filename="logs.txt",
        filemode="a",
        level=INFO,
        format_="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        date_format="%d-%b-%y %H:%M:%S",
    )
    # Auctions
    auctions_repository = providers.Singleton(
        # AuctionsRepository, db_url=config.auctions_repository.db_url()
        AuctionsRepository,
        db_url="mysql://user:password@db:3306/auctions",
    )

    create_auction_service = providers.Factory(
        CreateAuctionService, repository=auctions_repository, logger=logger
    )
