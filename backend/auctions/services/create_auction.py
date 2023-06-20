from datetime import datetime
from dataclasses import dataclass

from backend.auctions.models.auction import Auction
from backend.shared import ILogger, IGenericRepository


@dataclass(frozen=True)
class CreateAuctionDto:
    id: int
    title: str
    starting_price: float
    ends_at: datetime


class CreateAuctionService:
    def __init__(self, *, repository: IGenericRepository, logger: ILogger) -> None:
        self._repository = repository
        self._logger = logger

    def execute(self, *, input_dto: CreateAuctionDto) -> None:
        auction = Auction(
            title=input_dto.title,
            starting_price=input_dto.starting_price,
            ends_at=input_dto.ends_at,
        )

        added = self._repository.add(auction=auction)
        self._logger.info(message="Auction created")

        return added
