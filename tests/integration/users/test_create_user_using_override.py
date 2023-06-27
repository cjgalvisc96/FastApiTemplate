from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.shared import encypt_password
from backend.users import User, SQLAlchemyUsersRepositoryImp


@pytest.fixture
def client():
    yield TestClient(app=app, base_url="http://test")


@pytest.fixture
def token_admin(client):
    repository_mock = Mock(spec=SQLAlchemyUsersRepositoryImp)
    email = "admin@gmail.com"
    repository_mock.get_by_filter.return_value = User(
        name="admin",
        lastname="admin",
        email=email,
        hashed_password=encypt_password(password='admin'),
        active=True,
    )
    with app.container.users_repository.override(repository_mock):
        authentication_response = client.post(
            url="/v1/users/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "",
                "client_id": "",
                "client_secret": "",
                "username": "admin@gmail.com",
                "password": "admin",
                "scope": "users:all",
            },
        )

    assert authentication_response.status_code == 200
    repository_mock.get_by_filter.assert_called_once_with(filter_={'email': email})

    return authentication_response.json()['access_token']


def test_create_a_valid_user(token_admin, client):
    repository_mock = Mock(spec=SQLAlchemyUsersRepositoryImp)
    repository_mock.add.return_value = User(
        id=1,
        name="TestName",
        lastname="TestLastname",
        email="test@gmail.com",
        hashed_password=encypt_password(password='TestPassword'),
        active=True,
    )
    with app.container.users_repository.override(repository_mock):
        users_response = client.post(
            url="/v1/users/1",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_admin}",
            },
            json={
                "name": "TestName",
                "lastname": "TestLastname",
                "email": "test@gmail.com",
                "password": "TestPassword",
            },
        )

    repository_mock.add.assert_called_once()

    assert users_response.status_code == 201
    assert users_response.json() == {
        "name": "TestName",
        "lastname": "TestLastname",
        "email": "test@gmail.com",
    }
