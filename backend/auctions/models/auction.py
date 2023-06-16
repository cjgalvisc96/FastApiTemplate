from datetime import datetime
from dataclasses import dataclass


@dataclass
class Auction:
    id: int
    title: str
    starting_price: float
    bids: list[int]
    ends_at: datetime