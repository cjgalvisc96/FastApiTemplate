from typing import Callable
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session


class SQLAlchemyRepository:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(url=db_url, echo=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

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
