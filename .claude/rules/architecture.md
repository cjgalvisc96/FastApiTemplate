# Architecture rules

The codebase uses **dependency injection** (`dependency-injector`) and the **repository pattern**,
organized into feature modules. Follow the existing layering — don't reach around it.

## Layering (per feature, e.g. `backend/users/`)
```
api/         HTTP layer: routers, request validators, response serializers.
services/    Business logic. Depends on a repository via an abstract interface.
repository.py  Data access: implements backend.shared.interfaces.GenericRepository.
models.py    SQLAlchemy models.
tasks.py     Celery tasks.
```
Rules:
- **API handlers** parse/validate input, build a DTO, call a service, and translate errors into
  `GeneralAPIException`. No business logic or direct DB access in endpoints.
- **Services** hold business logic and depend on `GenericRepository` (the abstract interface from
  `backend/shared`), never on a concrete repository class. Inputs come in as frozen dataclass DTOs
  (see `CreateUserDto`). Keyword-only args (`def create_user(self, *, input_dto: ...)`).
- **Repositories** implement `GenericRepository` and are the only place that touches the DB session.
  They use the injected `session_factory` context manager and raise `NotFoundError` on misses.

## Dependency injection
- All wiring lives in `backend/container.py` (`ApplicationContainer`). Register new repositories and
  services there as `providers.Factory(...)`, wiring dependencies from other providers (e.g.
  `users_service = providers.Factory(UsersService, repository=users_repository)`).
- Singletons for shared resources (`db`, `fastapi_redis_cache`); factories for per-request services.
- Endpoints receive dependencies via `Depends(Provide[ApplicationContainer.<provider>])` and the
  `@inject` decorator. `wiring_config` in the container lists wired packages (e.g. `.users`).
- Config is provided via `providers.Configuration(pydantic_settings=[settings])`; read values as
  `config.<section>.<KEY>`.

## Adding a new feature module
1. Create `backend/<feature>/` with `api/`, `services/`, `repository.py`, `models.py`, and an
   `__init__.py` that re-exports the module's public names (services, DTOs, repository impl).
2. Implement the repository against `GenericRepository`; put business logic in services with DTOs.
3. Register the repository + services as providers in `backend/container.py` and add the feature to
   `wiring_config.packages`.
4. Add the router to `add_routers(...)` in `backend/app.py` (routes are prefixed `/v1`).
5. Register any DB init / cache init needs through the startup events in `app.py`.

## Errors
- Domain/repository misses raise `NotFoundError` (from `backend/shared/interfaces/repository.py`).
- API-facing failures raise `GeneralAPIException(code=..., message=...)`, handled centrally in
  `app.py` and returned as `{"error": {"code", "message"}, "data": null}` with HTTP 400.
