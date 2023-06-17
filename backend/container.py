from logging import INFO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from dependency_injector import providers, containers

from backend.shared import LoggingLogger
from backend.auctions import AuctionsRepository, AuctionsUnitOfWork, CreateAuctionService


class ApplicationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".auctions.api.create_auction"])
    # wiring_config = containers.WiringConfiguration(
    #     packages=["auctions"]
    # )
    # General
    logger = logger = providers.Singleton(
        LoggingLogger,
        name="BackendLogger",
        filename="logs.txt",
        filemode="a",
        level=INFO,
        format_="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        date_format="%d-%b-%y %H:%M:%S",
    )

    # Auctions
    DEFAULT_SESSION_FACTORY = sessionmaker(
        bind=create_engine('mysql://user:password@db:3306/auctions'),
    )
    auctions_uow = providers.Singleton(
        AuctionsUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
        repository=AuctionsRepository
    )
    create_auction_service = providers.Factory(
        CreateAuctionService, uow=auctions_uow, logger=logger
    )
