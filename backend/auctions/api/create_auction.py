from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from fastapi import status, Depends, APIRouter
from dependency_injector.wiring import inject, Provide

from backend.shared import GeneralAPIException
from backend.auctions import CreateAuctionDto, CreateAuctionService

# from backend.container import ApplicationContainer


create_auction_router = APIRouter(tags=["CreateAuctions"])


class AuctionPostValidator(BaseModel):
    title: str
    starting_price: float
    bids: Optional[list[int]]
    ends_at: Optional[datetime]


@create_auction_router.post("/{auction_id}", status_code=status.HTTP_201_CREATED)
@inject
async def create_auction(
    auction_id: int,
    auction: AuctionPostValidator,
    # create_auctions_service: CreateAuctionService = Depends(Provide[ApplicationContainer.create_auction_service]),
    create_auctions_service=CreateAuctionService,
):
    return {}
    # input_dto = CreateAuctionDto(id=auction_id, **auction)
    # try:
    #     create_auctions_service(input_dto=input_dto)
    # except Exception as error:
    #     raise GeneralAPIException(code="test", message=error)
