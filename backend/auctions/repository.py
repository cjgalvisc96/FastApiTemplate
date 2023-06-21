from typing import Any, Iterator

from backend.auctions import Auction
from backend.shared import NotFoundError, IGenericRepository, SQLAlchemyDatabase


class SQLAlchemyAuctionsRepository(SQLAlchemyDatabase, IGenericRepository):
    def add(self, *, auction: Auction) -> Auction:
        with self._session_factory() as session:
            session.add(auction)
            session.commit()
            session.refresh(auction)
            return auction

    def get_all(self) -> Iterator[Auction]:
        with self._session_factory() as session:
            return session.query(Auction).all()

    def get_by_id(self, id: int) -> Auction:
        with self._session_factory() as session:
            auction = session.get(Auction, id)
            if not auction:
                raise NotFoundError(id)

            return auction

    def get_by_filter(self, filter_: dict[str, Any]) -> Auction:
        with self._session_factory() as session:
            auction = session.query(Auction).filter_by(**filter_)
            if not auction:
                raise NotFoundError(0)

            return auction.first()

    def update_by_id(self, id: int, data_to_update: dict[str, Any]) -> Auction:
        auction = self.get_by_id(id=id)
        with self._session_factory() as session:
            auction.update(data_to_update)
            session.commit()
            session.refresh(auction)

    def remove_by_id(self, id: int) -> None:
        auction = self.get_by_id(id=id)
        with self._session_factory() as session:
            session.delete(auction)
            session.commit()
