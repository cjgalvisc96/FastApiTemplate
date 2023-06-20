from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide
from fastapi import status, Depends, Response, APIRouter

from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer
from backend.auctions import AuctionsService, CreateAuctionDto

auctions_router = APIRouter(prefix="/auctions", tags=["Auctions"])

MEDIA_TYPE = 'application/json'


class AuctionPostValidator(BaseModel):
    title: str
    starting_price: int
    bids: Optional[list[int]]
    ends_at: Optional[datetime]


@auctions_router.post("/{auction_id}", status_code=status.HTTP_201_CREATED)
@inject
async def create_auction(
    auction_id: int,
    auction: AuctionPostValidator,
    auctions_service: AuctionsService = Depends(Provide[ApplicationContainer.auctions_service]),
):
    input_dto = CreateAuctionDto(
        id=auction_id,
        title=auction.title,
        starting_price=auction.starting_price,
        ends_at=datetime.now() + timedelta(days=1),
    )
    try:
        auctions_service.create_auction(input_dto=input_dto)
    except Exception as error:
        raise GeneralAPIException(code="test", message=str(error))


@auctions_router.get("/{auction_id}", status_code=status.HTTP_200_OK)
@inject
async def get_auction(
    auction_id: int,
    auctions_service: AuctionsService = Depends(Provide[ApplicationContainer.auctions_service]),
):
    try:
        auction = await auctions_service.get_auction(id=auction_id)
    except Exception as error:
        raise GeneralAPIException(code="test", message=str(error))

    return Response(content=auction, media_type=MEDIA_TYPE)
