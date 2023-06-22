from typing import Any
from dataclasses import dataclass

from backend.users.models import User
from backend.shared import ILogger, IGenericRepository


@dataclass(frozen=True)
class CreateUserDto:
    id: int
    name: str
    lastname: str
    email: str
    password: str


class UsersService:
    def __init__(self, *, repository: IGenericRepository, logger: ILogger) -> None:
        self._repository = repository
        self._logger = logger

    def create_user(self, *, input_dto: CreateUserDto) -> User:
        user = User(
            name=input_dto.name,
            lastname=input_dto.lastname,
            email=input_dto.email,
            hashed_password=input_dto.password,
        )

        user_created = self._repository.add(user=user)
        self._logger.info(message="User created")

        return user_created

    def get_user_by_filter(self, *, filter_: dict[str, Any]) -> User:
        return self._repository.get_by_filter(filter_=filter_)

    def get_user(self, *, id: int) -> User:
        return self._repository.get_by_id(id=id)
