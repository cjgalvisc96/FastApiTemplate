import logging
from typing import Callable
from datetime import datetime
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy.orm import Session, registry, sessionmaker, scoped_session
from sqlalchemy import Table, Column, String, Boolean, Integer, DateTime, MetaData, create_engine

logger = logging.getLogger(name=__name__)


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
            # timestamps
            # TODO: Apply DRY
            Column('active', Boolean, default=True),
            Column('created_at', DateTime, default=datetime.now),
            Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now),
        )
        users = Table(
            'users',
            mapper_registry.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(20)),
            Column('lastname', String(20)),
            Column('email', String(50), unique=True, nullable=False),
            Column('hashed_password', String(100)),
            # timestamps
            # TODO: Apply DRY
            Column('active', Boolean, default=True),
            Column('created_at', DateTime, default=datetime.now),
            Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now),
        )

        from backend.users import User
        from backend.auctions import Auction

        mapper_registry.map_imperatively(Auction, auctions)
        mapper_registry.map_imperatively(User, users)

        mapper_registry.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as error:
            logger.error(msg="Session rollback because of exception")
            session.rollback()
            raise error
        finally:
            session.close()
