# FastApiTemplate
Template to create FastApi projects using dependency injection and repository pattern.
## How to install the app?
**Prerequisites**: 
[Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
```sh
    [root_directory] make up
```
## How to install from scratch?
```sh
    [root_directory] make install_from_scratch
```
## How to reboot the app?
```sh
    [root_directory] make reboot
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
```sh
    [root_directory] make test_db_sh
```

## How to down the app?
```sh
    [root_directory] make down 
```

# TODO:

Missing:
    Resolve TODOs(Fix poetry dependencies)
