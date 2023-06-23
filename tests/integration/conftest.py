import logging
from json import loads

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import then, given, parsers

from backend.app import app

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    with TestClient(app=app, base_url="http://test") as client:
        yield client


@given(
    parsers.parse(
        'I authenticate using the following credentials:\n{credentials:json}',
        extra_types=dict(json=loads),
    ),
    target_fixture="http_request",
)
def authenticate_user(client, credentials):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {"grant_type": "", "client_id": "", "client_secret": ""}
    data.update(credentials)

    authenticate_endpoint = "/v1/users/token"

    http_request = client.post(url=authenticate_endpoint, headers=headers, data=data)

    return http_request


@given(
    parsers.parse(
        'I send a POST request to "{endpoint}" with body:\n{body:json}',
        extra_types=dict(json=loads),
    ),
    target_fixture="http_request",
)
def send_post_request(http_request, client, endpoint, body):
    headers = {}
    if http_request.status_code == 200:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {http_request.json()['access_token']}",
        }

    http_request = client.post(url=endpoint, headers=headers, json=body)
    return http_request


@then(parsers.parse('The response status code should be "{expected_response_status:d}"'))
def check_response_status(http_request, expected_response_status):
    assert http_request.status_code == expected_response_status


@then(
    parsers.parse(
        "The response body should be:\n{expected_response_body:json}",
        extra_types=dict(json=loads),
    )
)
def check_response_body(http_request, expected_response_body):
    assert http_request.json() == expected_response_body
