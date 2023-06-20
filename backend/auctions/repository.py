from typing import Any, Callable, Iterator
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from backend.auctions.models.auction import Auction
from backend.shared import NotFoundError, IGenericRepository

Base = declarative_base()


class AuctionsRepository(IGenericRepository):
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(url=db_url, echo=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as error:
            # logger.exception("Session rollback because of exception")
            session.rollback()
            raise error
        finally:
            session.close()

    def add(self, *, auction: Auction) -> Auction:
        with self._session_factory() as session:
            session.add(auction)
            session.commit()
            session.refresh()
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
