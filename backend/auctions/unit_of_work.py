from typing import Self

from sqlalchemy.orm import sessionmaker

from backend.shared import IUnitOfWork, IGenericRepository


class AuctionsUnitOfWork(IUnitOfWork):
    def __init__(
        self,
        repository: IGenericRepository,
    ) -> None:
        self.repository = repository
        self._session = None

    def __enter__(self) -> Self:
        self._session = self.repository.session_factory()
        return self

    def __exit__(self, *args) -> None:
        self._session.rollback()
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
