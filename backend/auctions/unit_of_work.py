from typing import Self

from backend.shared import (
    _default_session_factory,
    IUnitOfWork,
)
from backend.auctions.repository import AuctionsRepository



class AuctionsUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory=_default_session_factory) -> None:
        self._session_factory = session_factory

    def __enter__(self) -> Self:
        self._session = self._session_factory()

        self.accounts = AuctionsRepository(self._session)

        return self

    def __exit__(self, *args) -> None:
        self._session.rollback()
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()