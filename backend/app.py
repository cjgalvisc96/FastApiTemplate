from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fever_events.constants import APPLICATION_API
from fever_events.container import Container
from fever_events.infrastructure.application_api.api_v1.events import (
    router as events_router,
)
from fever_events.infrastructure.application_api.api_v1.exceptions import (
    GeneralAPIException,
)


def add_routers(*, app: FastAPI) -> None:
    app.include_router(
        router=events_router, prefix=APPLICATION_API["API_VERSION_PREFIX"]
    )


def add_middleware(*, app: FastAPI) -> None:
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_handle_exceptions(*, app: FastAPI) -> None:
    @app.exception_handler(GeneralAPIException)
    async def general_exception(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {"code": exc.code, "message": exc.message},
                "data": None,
            },
        )


def add_dependency_injection(*, app: FastAPI, container: object) -> None:
    app.container = container


def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()

    add_dependency_injection(app=app, container=container)
    add_routers(app=app)
    add_middleware(app=app)
    add_handle_exceptions(app=app)
    return app


app = create_app()
