from sqlalchemy import Column, String, Integer, DateTime

from backend.shared import Base


class Auction(Base):
    __tablename__ = "auctions"

    id: Column(Integer, primary_key=True)
    title: Column(String)
    starting_price: Column(Integer)  # Cents
    bids: Column(String)
    ends_at: Column(DateTime)

    def __repr__(self):
        return (
            f"<Auction(id={self.id}, "
            f"title=\"{self.title}\", "
            f"starting_price=\"{self.starting_price}\", "
            f"bids=\"{self.bids}\", "
            f"ends_at={self.ends_at})>"
        )
