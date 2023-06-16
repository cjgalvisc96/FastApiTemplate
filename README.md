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

## How to enter in the app container?
```sh
    [root_directory] make sh
```

## How to down the app?
```sh
    [root_directory] make down 
```