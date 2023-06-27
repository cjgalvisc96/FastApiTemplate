import logging
from typing import Callable
from contextlib import contextmanager, AbstractContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from backend.shared.utils import encypt_password
from backend.shared.exceptions import SQLAlchemyException

logger = logging.getLogger(name=__name__)

Base = declarative_base()


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
        Base.metadata.create_all(self._engine)
        self.insert_default_records()

    def insert_default_records(self) -> None:
        from backend.users import User

        records_to_insert = (
            {
                "model": User,
                "record": User(
                    name="admin",
                    lastname="admin",
                    email="admin@gmail.com",
                    hashed_password=encypt_password(password='admin'),
                ),
                "filter": {'email': 'admin@gmail.com'},
            },
        )
        with self.session() as session:
            for record_to_insert in records_to_insert:
                if record_to_insert["filter"]:
                    record = (
                        session.query(record_to_insert["model"])
                        .filter_by(**record_to_insert["filter"])
                        .first()
                    )

                if record is None or not record:
                    session.add(record_to_insert["record"])
                    session.commit()
                    session.refresh(record_to_insert["record"])

        logger.info("Default DB data created sucessfull!")

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as error:
            logger.error(msg=f"DB Session rollback because of exception={error}")
            session.rollback()
            raise SQLAlchemyException(f"DB error={error}")
        finally:
            session.close()
