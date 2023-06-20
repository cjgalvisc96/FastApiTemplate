from datetime import datetime
from dataclasses import dataclass

from backend.auctions.models.auction import Auction
from backend.shared import ICache, ILogger, IGenericRepository


@dataclass(frozen=True)
class CreateAuctionDto:
    id: int
    title: str
    starting_price: float
    ends_at: datetime


class AuctionsService:
    def __init__(self, *, repository: IGenericRepository, logger: ILogger, cache: ICache) -> None:
        self._repository = repository
        self._logger = logger
        self._cache = cache.get_cache()

    def create_auction(self, *, input_dto: CreateAuctionDto) -> Auction:
        auction = Auction(
            title=input_dto.title,
            starting_price=input_dto.starting_price,
            ends_at=input_dto.ends_at,
        )

        added = self._repository.add(auction=auction)
        self._logger.info(message="Auction created")

        return added

    async def get_auction(self, *, id: int) -> Auction:
        auction_in_cache = await self._cache.get('auction_in_cache')
        if auction_in_cache:
            return auction_in_cache

        auction = self._repository.get_by_id(id=id)
        await self._cache.set('auction_in_cache', auction.to_str())
        return auction
