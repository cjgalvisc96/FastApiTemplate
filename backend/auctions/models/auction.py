from datetime import datetime
from dataclasses import asdict, dataclass


@dataclass
class Auction:
    title: str
    starting_price: int
    ends_at: datetime

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

    def to_str(self):
        return str(self.to_dict())
