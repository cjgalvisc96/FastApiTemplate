from fastapi import APIRouter

from backend.auctions.api.create_auction import router as create_auction_router

auctions_router = APIRouter(prefix="/auctions", tags=["Auctions"])


auctions_router.include_router(router=create_auction_router)
