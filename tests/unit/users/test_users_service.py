import logging
from unittest.mock import Mock

import pytest

from tests.unit.mothers import UserMother
from backend.shared.utils import encypt_password
from backend.users import UsersService, SQLAlchemyUsersRepositoryImp


@pytest.mark.unit
def test_create_user(caplog):
    user_mother = UserMother()
    input_dto = user_mother.create_valid_user_dto()
    excepted_db_user_created = user_mother.create_valid_db_user(
        data={
            "id": input_dto.id,
            "name": input_dto.name,
            "lastname": input_dto.lastname,
            "email": input_dto.email,
            "hashed_password": encypt_password(password=input_dto.password),
            "active": True,
        }
    )

    users_repository_mock = Mock(spec=SQLAlchemyUsersRepositoryImp)
    users_repository_mock.add.return_value = excepted_db_user_created
    users_service = UsersService(repository=users_repository_mock)
    user_created = users_service.create_user(input_dto=input_dto)

    assert user_created == excepted_db_user_created
    assert (
        caplog.record_tuples.count(('backend.users.services.users', logging.INFO, "User created"))
        == 1
    )
    users_repository_mock.add.assert_called_once()
