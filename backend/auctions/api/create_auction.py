from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel
from fastapi import status, Depends, APIRouter
from dependency_injector.wiring import inject, Provide

from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer
from backend.auctions import CreateAuctionDto, CreateAuctionService

create_auction_router = APIRouter()


class AuctionPostValidator(BaseModel):
    title: str
    starting_price: int
    bids: Optional[list[int]]
    ends_at: Optional[datetime]


@create_auction_router.post("/{auction_id}", status_code=status.HTTP_201_CREATED)
@inject
async def create_auction(
    auction_id: int,
    auction: AuctionPostValidator,
    create_auctions_service: CreateAuctionService = Depends(
        Provide[ApplicationContainer.create_auction_service]
    ),
):
    input_dto = CreateAuctionDto(
        id=auction_id,
        title=auction.title,
        starting_price=auction.starting_price,
        ends_at=datetime.now() + timedelta(days=1),
    )
    try:
        create_auctions_service.execute(input_dto=input_dto)
    except Exception as error:
        raise GeneralAPIException(code="test", message=str(error))
