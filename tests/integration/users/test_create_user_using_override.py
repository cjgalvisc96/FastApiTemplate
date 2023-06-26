from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.shared import encypt_password
from backend.users import User, SQLAlchemyUsersRepositoryImp


@pytest.fixture
def client():
    yield TestClient(app=app, base_url="http://test")


def test_create_a_valid_user(client):
    repository_mock = Mock(spec=SQLAlchemyUsersRepositoryImp)
    repository_mock.get_by_filter.return_value = User(
        name="admin",
        lastname="admin",
        email="admin@gmail.com",
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
    repository_mock.get_by_filter.assert_called_once_with(filter_={'email': "admin@gmail.com"})

    body = {
        "name": "TestName",
        "lastname": "TestLastname",
        "email": "test@gmail.com",
        "password": "TestPassword",
    }
    repository_mock.get_by_filter.return_value = User(
        name="admin",
        lastname="admin",
        email="admin@gmail.com",
        hashed_password=encypt_password(password='admin'),
        active=True,
    )
    hashed_password = encypt_password(password='TestPassword')
    repository_mock.add.return_value = User(
        name="TestName",
        lastname="TestLastname",
        email="test@gmail.com",
        hashed_password=hashed_password,
        active=True,
    )
    with app.container.users_repository.override(repository_mock):
        users_response = client.post(
            url="/v1/users/1",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {authentication_response.json()['access_token']}",
            },
            json=body,
        )

    assert users_response.status_code == 201
    repository_mock.add.assert_called_once()

    assert 5 > 4
    assert users_response.json() == {
        "name": "TestName",
        "lastname": "TestLastname",
        "email": "test@gmail.com",
    }
