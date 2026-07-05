# FastApiTemplate

FastAPI template built around **dependency injection** (`dependency-injector`) and the
**repository pattern**, organized into feature modules. MySQL via SQLAlchemy, Redis cache,
Celery workers/beat. Python ^3.10, managed with Poetry, run through Docker Compose.

## Layout
- `backend/` — application code, organized by feature.
  - `backend/app.py` — FastAPI app factory (`create_app`), routers, middleware, exception handler,
    startup/shutdown events.
  - `backend/container.py` — the `ApplicationContainer` DI wiring (providers for repositories,
    services, db, cache).
  - `backend/config/` — settings (`config.py`) and Celery config.
  - `backend/shared/` — cross-cutting code: `interfaces/` (abstract `GenericRepository`, cache),
    `sqlalchemy_repository.py`, `SQLAlchemyDatabase`, cache impl, exceptions, utils.
  - `backend/users/` — example feature module: `api/` (endpoints, serializers, validators),
    `services/` (business logic), `repository.py` (data access), `models.py`, `tasks.py`.
- `tests/` — `tests/unit/` and `tests/integration/`, mirroring the feature layout.

## Common commands (via `Makefile`, run in Docker)
- `make up` / `make down` — start / stop the dev stack.
- `make test` — run the full pytest suite in the backend container.
- `make coverage` — run tests with coverage and print the report.
- `make linter_apply` — run isort + black. `make linter_check` — verify formatting.
- `make backend_sh` / `make db_sh` — shell into the backend / db container.
- `make logs` — tail backend logs.

## Conventions
Detailed rules are split into topic files — read the relevant one before non-trivial work:
- @.claude/rules/architecture.md — DI + repository pattern, module layering, how to add a feature.
- @.claude/rules/testing.md — pytest unit/integration split, fixtures, mothers, pytest-bdd.
- @.claude/rules/style.md — formatting, imports, and code idioms used across the codebase.

## Specialist agents
`.claude/agents/` defines `architect` (design), `dev` (implementation), `tester` (tests), and
`lead` (orchestration). Delegate larger or cross-cutting work to `lead`.
