from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime

Base = declarative_base()


class Auction(Base):
    __tablename__ = "auction"

    id = Column(Integer(), primary_key=True)
    title = Column(String(20))
    starting_price = Column(Integer())  # Cents
    ends_at = Column(DateTime())
