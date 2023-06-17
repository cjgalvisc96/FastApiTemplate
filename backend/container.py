from logging import INFO

from dependency_injector import providers, containers

from backend.shared import Database, LoggingLogger
from backend.auctions import AuctionsRepository, AuctionsUnitOfWork, CreateAuctionService


class ApplicationContainer(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(modules=[".auctions.api.create_auction"])
    wiring_config = containers.WiringConfiguration(packages=[".auctions"])
    # General
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
    database = providers.Singleton(Database, db_url='mysql://user:password@db:3306/auctions')
    auctions_repository = providers.Singleton(
        AuctionsRepository, session_factory=database.provided.session
    )

    auctions_uow = providers.Factory(AuctionsUnitOfWork, repository=auctions_repository)

    create_auction_service = providers.Factory(
        CreateAuctionService, uow=auctions_uow, logger=logger
    )
