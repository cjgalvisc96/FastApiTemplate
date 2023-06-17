from typing import Self

from sqlalchemy.orm import sessionmaker

from backend.shared import IUnitOfWork, IGenericRepository


class AuctionsUnitOfWork(IUnitOfWork):
    def __init__(
        self,
        session_factory: sessionmaker,
        repository: IGenericRepository,
    ) -> None:
        self._session_factory = session_factory
        self.repository = repository

    def __enter__(self) -> Self:
        self._session = self._session_factory()
        self.repository(self._session)
        return self

    def __exit__(self, *args) -> None:
        self._session.rollback()
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
