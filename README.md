# FastApiTemplate
Template to create MVC FastApi projects

Create `Develop` branch

```sh
poetry add black isort pytest coverage fastapi uvicorn[standard] pydantic 
```

# Docs Template

## How to install the app?
**Prerequisites**: 
[Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
```sh
    [root_directory] make up
```
## How to run the tests?
```sh
    [root_directory] make tests
```

## How to run the coverage report?
```sh
    [root_directory] make coverage
```
## How to check the logs?
```sh
    [root_directory] make logs
```

## How to enter in the app containers?
```sh
    [root_directory] make backend_sh
```
```sh
    [root_directory] make db_sh
```

## How to down the app?
```sh
    [root_directory] make down 
```

# TODO:

Missing:
    Use Factory pattern in tests.
    Replace black by Ruff like a pylinter.

DDD Version:
    Add and inject Presenters services and selectors.

Resolve TODOs