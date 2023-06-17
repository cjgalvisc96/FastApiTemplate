from backend.shared import ILogger, IUnitOfWork

class GetAuctionService:
    def __init__(self, *, uow: IUnitOfWork, logger: ILogger) -> None:
        self._uow = uow
        self._logger = logger

    def execute(self) -> None:
        with self._uow:
            getted = self._uow.repository.get()

        self._logger.info(msg="Get Auction")
        return getted
