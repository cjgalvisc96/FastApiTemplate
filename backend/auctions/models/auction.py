from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime

from backend.shared import Base


class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer(), primary_key=True)
    title = Column(String(20))
    starting_price = Column(Integer())  # Cents
    ends_at = Column(DateTime())
