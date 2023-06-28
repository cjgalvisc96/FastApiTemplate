from json import loads

from pytest_bdd import then, given, parsers


@given(
    parsers.parse(
        'I authenticate using the following credentials:\n{credentials:json}',
        extra_types=dict(json=loads),
    ),
    target_fixture="token_user",
)
def token_user(client, credentials):
    http_request = client.post(
        url="/v1/users/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "", "client_id": "", "client_secret": ""} | credentials,
    )

    assert http_request.status_code == 200

    return http_request.json()['access_token']


@given(
    parsers.parse(
        'I send a POST request to "{endpoint}" with body:\n{body:json}',
        extra_types=dict(json=loads),
    ),
    target_fixture="http_request",
)
def send_post_request(token_user, client, endpoint, body):
    http_request = client.post(
        url=endpoint,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token_user}",
        },
        json=body,
    )
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
