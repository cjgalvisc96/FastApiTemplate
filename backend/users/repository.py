from typing import Any, Iterator

from backend.users.models import User
from backend.shared import NotFoundError, GenericRepository, SQLAlchemyDatabase


class SQLAlchemyUsersRepositoryImp(SQLAlchemyDatabase, GenericRepository):
    def add(self, *, user: User) -> User:
        with self._session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_all(self) -> Iterator[User]:
        with self._session_factory() as session:
            return session.query(User).all()

    def get_by_id(self, id: int) -> User:
        with self._session_factory() as session:
            user = session.get(User, id)
            if not user:
                raise NotFoundError(id)

            return user

    def get_by_filter(self, filter_: dict[str, Any]) -> User:
        with self._session_factory() as session:
            user = session.query(User).filter_by(**filter_)
            if not user:
                raise NotFoundError(0)

            return user.first()

    def update_by_id(self, id: int, data_to_update: dict[str, Any]) -> User:
        user = self.get_by_id(id=id)
        with self._session_factory() as session:
            user.update(data_to_update)
            session.commit()
            session.refresh(user)

    def remove_by_id(self, id: int) -> None:
        user = self.get_by_id(id=id)
        with self._session_factory() as session:
            session.delete(user)
            session.commit()
