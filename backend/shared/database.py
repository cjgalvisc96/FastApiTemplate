from typing import Callable
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy.orm import Session
from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base

# import logging


# logger = logging.getLogger(__name__)

class Base:
    __allow_unmapped__ = True


Base = declarative_base(cls=Base)


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
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
