from datetime import datetime
from dataclasses import dataclass

from backend.shared import ILogger, IUnitOfWork


@dataclass(frozen=True)
class CreateAuctionDto:
    id: int
    title: str
    starting_price: float
    bids: list[int]
    ends_at: datetime


class CreateAuctionService:
    def __init__(self, *, uow: IUnitOfWork, logger: ILogger) -> None:
        self._uow = uow
        self._logger = logger

    def execute(self, *, input_dto: CreateAuctionDto) -> None:
        with self._uow:
            added = self._uow.repository.add(auction=input_dto)

        self._logger.info(msg="Auction created")
        return added
