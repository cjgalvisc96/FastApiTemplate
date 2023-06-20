from datetime import datetime
from dataclasses import dataclass


@dataclass
class Auction:
    title: str
    starting_price: int
    ends_at: datetime
