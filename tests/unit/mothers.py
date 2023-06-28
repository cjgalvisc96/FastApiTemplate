from faker import Faker

from backend.users import User, CreateUserDto
from backend.shared.utils import encypt_password

faker_provider = Faker(locale="en_us")


class UserMother:
    def __init__(self, _faker_provider: Faker = faker_provider) -> None:
        self._faker_provider = faker_provider

    def create_valid_db_user(self, data=None):
        if data:
            return User(**data)

        return User(
            id=self._faker_provider.pyint(max_value=100),
            name=self._faker_provider.name(),
            lastname=self._faker_provider.last_name(),
            email=self._faker_provider.email(),
            hashed_password=encypt_password(self._faker_provider.password()),
            active=True,
        )

    def create_valid_user_dto(self, data=None):
        if data:
            return CreateUserDto(**data)

        return CreateUserDto(
            id=self._faker_provider.pyint(max_value=100),
            name=self._faker_provider.name(),
            lastname=self._faker_provider.last_name(),
            email=self._faker_provider.email(),
            password=self._faker_provider.password(),
        )
