# Style rules

Formatting is enforced by **black** and **isort** (config in `pyproject.toml`). Run
`make linter_apply` to format and `make linter_check` to verify. Always leave code passing the check.

## Formatting
- **black**: line length **100**, `target-version = py310`, `skip-string-normalization = true`
  (single quotes are kept — don't mass-convert quote style).
- **isort**: `profile = black`, sections `FUTURE, STDLIB, THIRDPARTY, FIRSTPARTY, LOCALFOLDER`,
  `length_sort = true`, `force_sort_within_sections = true`, trailing commas, reverse relative.
  Let isort order imports — don't hand-sort against it. `__init__.py` files are skipped.

## Idioms used across the codebase
- **Keyword-only arguments** for functions/methods with more than a trivial signature
  (`def create_user(self, *, input_dto: CreateUserDto)`, `def add_routers(*, app, routers)`).
  Call with keywords to match (`logger.info(msg=...)`, `encypt_password(password=...)`).
- **DTOs** are `@dataclass(frozen=True)` (e.g. `CreateUserDto`) for passing data into services.
- **Type hints** everywhere, using `X | Y` unions and builtin generics (`list[T]`, `dict[str, Any]`)
  — Python 3.10 style.
- **Module `__init__.py`** re-exports the feature's public API so other modules import from the
  package root (e.g. `from backend.users import UsersService, SQLAlchemyUsersRepositoryImp`).
- Loggers via `logging.getLogger(name=__name__)` at module top.

## Naming
- Repository implementations end in `...RepositoryImp` and implement `GenericRepository`.
- Services end in `...Service`; DTOs end in `...Dto`; API serializers end in `...Serializer`,
  validators in `...Validator` / `...Payload...`.
- Note existing typos are load-bearing for imports (e.g. `UserSerlializer`, `encypt_password`) —
  match the actual symbol names; don't "fix" them in passing without updating all references.
