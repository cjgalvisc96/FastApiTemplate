from typing import Any, Iterator

from sqlalchemy.orm import registry
from sqlalchemy import Table, Column, String, Integer, DateTime, MetaData

from backend.auctions import Auction
from backend.auctions.models.auction import Auction
from backend.shared import NotFoundError, IGenericRepository, SQLAlchemyRepository


class SQLAlchemyAuctionsRepository(SQLAlchemyRepository, IGenericRepository):
    def create_database(self) -> None:
        meta = MetaData()
        mapper_registry = registry(metadata=meta)
        auctions = Table(
            'auctions',
            mapper_registry.metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String(20)),
            Column('starting_price', Integer),
            Column('ends_at', DateTime),
        )
        mapper_registry.map_imperatively(Auction, auctions)
        mapper_registry.metadata.create_all(bind=self._engine)

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

    def update_by_id(self, id: int, data_to_update: dict[str, Any]) -> Auction:
        with self._session_factory() as session:
            auction = session.get(Auction, id)
            if not auction:
                raise NotFoundError(id)

            auction.update(data_to_update)
            session.commit()
            session.refresh(auction)

    def remove_by_id(self, id: int) -> None:
        with self._session_factory() as session:
            auction = self.get_by_id(auction_id=id)
            session.delete(auction)
            session.commit()
