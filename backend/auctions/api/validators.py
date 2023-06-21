from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class AuctionPostValidator(BaseModel):
    title: str
    starting_price: int
    bids: Optional[list[int]]
    ends_at: Optional[datetime]
