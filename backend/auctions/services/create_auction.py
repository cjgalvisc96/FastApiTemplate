from datetime import datetime
from dataclasses import dataclass
from backend.auctions.models.auction import Auction
from backend.shared import ILogger, IUnitOfWork


@dataclass(frozen=True)
class CreateAuctionDto:
    id: int
    title: str
    starting_price: float
    ends_at: datetime


class CreateAuctionService:
    def __init__(self, *, uow: IUnitOfWork, logger: ILogger) -> None:
        self._uow = uow
        self._logger = logger

    def execute(self, *, input_dto: CreateAuctionDto) -> None:
        with self._uow:
            auction = Auction(
                id=input_dto.id,
                title=input_dto.title,
                starting_price=input_dto.starting_price,
                ends_at=input_dto.ends_at,
            )
            added = self._uow.repository.add(auction=auction)
            # self._uow.commit()

        self._logger.info(msg="Auction created")
        return added
