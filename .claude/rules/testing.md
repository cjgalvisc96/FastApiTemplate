# Testing rules

Runner is **pytest**, run inside the backend container via `make test` (full suite) or
`make coverage`. Tests live under `tests/`, split into `unit/` and `integration/`, mirroring the
feature layout under `backend/`.

## Markers
- `@pytest.mark.unit` — isolated tests of services/selectors with collaborators mocked.
- `@pytest.mark.integration` — tests exercising the API + real (test) DB.

## Unit tests
- Test a service in isolation. Mock its repository with `Mock(spec=SQLAlchemyUsersRepositoryImp)` and
  set `.return_value` on the methods it calls; assert calls with `assert_called_once()` etc.
- Build test data with **object mothers** in `tests/unit/mothers.py` (`UserMother`, backed by
  `faker`) — `create_valid_user_dto()`, `create_valid_db_user(data=...)`. Reuse and extend these
  rather than hand-building models inline.
- Assert on logging via the `caplog` fixture (set to INFO in `tests/conftest.py`); check
  `caplog.record_tuples`.

## Integration tests
- Use the `client` fixture (a `TestClient`) from `tests/conftest.py`. The `app_test` fixture
  overrides the `db` provider to point at `TEST_DB_URL`, and cleans + recreates the DB around each
  test — never point integration tests at the dev DB.
- Behavior is written with **pytest-bdd**: a `.feature` file (Gherkin) plus a small
  `@scenario(...)` binding in `test_*.py`. Reusable `given`/`then` steps live in
  `tests/integration/conftest.py` (auth, POST request, status/body assertions), parsing inline JSON
  via `parsers.parse(..., extra_types=dict(json=loads))`.
- To add an integration case: add a `Scenario` to the feature file (or a new `.feature`), reference
  it from a `@scenario`-decorated test, and reuse existing steps where possible.

## Expectations
- Add/adjust tests whenever behavior changes; keep the suite green.
- Cover happy path, validation/error paths, and edge cases. Don't weaken assertions to force a pass —
  investigate failures.
- Keep test code formatted with black/isort (line length 100), same as production code.
