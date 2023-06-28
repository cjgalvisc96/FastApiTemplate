import pytest
from pytest_bdd import scenario

FEAUTRE_NAME = "./create_user.feature"


@pytest.mark.integration
@scenario(
    feature_name=FEAUTRE_NAME,
    scenario_name="Create a valid user",
)
def test_create_a_valid_user():
    ...
