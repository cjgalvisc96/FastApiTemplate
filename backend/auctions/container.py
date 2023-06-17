from logging import INFO

from dependency_injector import providers, containers

from backend.shared import LoggingLogger, _default_session_factory
from backend.auctions import AuctionsRepository, AuctionsUnitOfWork, create_auction_service


class AuctionsContainer(containers.DeclarativeContainer):
    auctions_repository = providers.Singleton(AuctionsRepository)
    auctions_uow = providers.Singleton(
        AuctionsUnitOfWork, repository=auctions_repository, session_factory=_default_session_factory
    )
    logger = logger = providers.Singleton(
        LoggingLogger,
        name="BackendLogger",
        filename="logs.txt",
        filemode="a",
        level=INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
    )

    create_auction_service = providers.Factory(
        create_auction_service, uow=auctions_uow, logger=logger
    )
