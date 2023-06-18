from typing import Callable, Iterator
from contextlib import AbstractContextManager

from sqlalchemy.orm.session import Session

from backend.shared import IGenericRepository
from backend.auctions.models.auction import Auction


class AuctionsRepository(IGenericRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, *, entity) -> Auction:
        with self.session_factory() as session:
            auction = self.session.add(entity)
            return auction

    def get_all(self) -> Iterator[Auction]:
        with self.session_factory() as session:
            return session.query(Auction).all()

    def get_by_id(self, auction_id: int) -> Auction:
        with self.session_factory() as session:
            auction = session.get(Auction, id)
            if not auction:
                raise NotFoundError(auction_id)
            return auction

    def delete_by_id(self, auction_id: int) -> None:
        with self.session_factory() as session:
            auction = self.get_by_id(auction_id=auction_id)
            session.delete(auction)
            session.commit()


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")
