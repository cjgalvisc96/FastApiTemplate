from datetime import datetime
from fastapi import status, Depends, APIRouter
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from backend.shared import GeneralAPIException
from backend.auctions import CreateAuctionDto, CreateAuctionService
from backend.container import ApplicationContainer


router = APIRouter(prefix="", tags=["CreateAuctions"])


class AuctionPostValidator(BaseModel):
    title: str
    starting_price: float
    bids: list[int]
    ends_at: datetime


@router.post("/{auction_id}", status_code=status.HTTP_201_CREATED)
@inject
async def create_auction(
    product_id: int,
    auction: AuctionPostValidator,
    create_auctions_service: CreateAuctionService = Depends(Provide[ApplicationContainer.create_auction_service]),
):
    input_dto = CreateAuctionDto(id=product_id, **auction)
    try:
        create_auctions_service(input_dto=input_dto)
    except Exception as error:
        raise GeneralAPIException(code="test", message=error)

container = ApplicationContainer()
container.wire(modules=[__name__])