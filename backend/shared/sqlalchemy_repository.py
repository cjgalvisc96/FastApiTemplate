from typing import Callable
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy.orm import Session, registry, sessionmaker, scoped_session
from sqlalchemy import Table, Column, String, Integer, DateTime, MetaData, create_engine


class SQLAlchemyDatabase:
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
        from backend.auctions import Auction

        mapper_registry.map_imperatively(Auction, auctions)
        mapper_registry.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as error:
            # logger.error(message="Session rollback because of exception")
            session.rollback()
            raise error
        finally:
            session.close()
