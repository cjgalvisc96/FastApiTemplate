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

Finish this use cases:
    As an administrator I want to create auctions so that bidders can place bids on them.
    As a bidder I want to place a bid so that I can win the auction
    As a bidder I want to recieve e-mail notification when my bid is a winning one.
    As an administrator I want to withdraw bids so that a malicious bidder does not win as auction.

Missing:
    Finish app uow.
    USE BDD in integration tests.
    Use Factory pattern in tests.

    FastApi swagger docs.
    Celery Setup.
    Create "curl" commands to add in documentation.
    Add authentification jwt after to finish.

DDD Version:
    Add and inject Presenters services and selectors.