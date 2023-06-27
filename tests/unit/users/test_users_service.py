import logging
from unittest.mock import Mock

import pytest

from backend.users import User, UsersService, CreateUserDto, SQLAlchemyUsersRepositoryImp


@pytest.fixture
def caplog(caplog):
    caplog.set_level(logging.INFO)
    yield caplog
    caplog.clear()


def test_create_user(caplog):
    users_repository_mock = Mock(spec=SQLAlchemyUsersRepositoryImp)
    excepted_db_user_created = User(
        id=1,
        name="test",
        lastname="test",
        email="test@email.com",
        hashed_password="test",
        active=True,
    )
    users_repository_mock.add.return_value = excepted_db_user_created
    users_service = UsersService(repository=users_repository_mock)
    user_created = users_service.create_user(
        input_dto=CreateUserDto(
            id=1, name="test", lastname="test", email="test@email.com", password="test"
        )
    )

    assert user_created == excepted_db_user_created
    assert (
        caplog.record_tuples.count(('backend.users.services.users', logging.INFO, "User created"))
        == 1
    )
    users_repository_mock.add.assert_called_once()
