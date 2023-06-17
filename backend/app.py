import debugpy
from fastapi.responses import JSONResponse
from fastapi import status, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer
from backend.auctions.api.router import auctions_router


def attach_debug():
    debug_host = "0.0.0.0"
    debug_port = 9500
    debugpy.listen((debug_host, debug_port))
    print(f'DEBUG Attached!, running in: {debug_host}:{debug_port}')


def attach_test_debug_waiting_connection():
    debug_host = "0.0.0.0"
    debug_port = 9500
    debugpy.listen((debug_host, debug_port))
    print("Waiting for DEBUG attaching")
    debugpy.wait_for_client()
    print(f'DEBUG Attached!, running in: {debug_host}:{debug_port}')


def add_routers(*, app: FastAPI, routers: list[APIRouter]) -> None:
    for router in routers:
        app.include_router(router=router, prefix="/v1", tags=["application"])


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
    # attach_test_debug_waiting_connection()
    container = ApplicationContainer()
    db = container.database()
    db.create_database()

    attach_debug()
    app = FastAPI()

    add_dependency_injection(app=app, container=container)
    add_routers(app=app, routers=[auctions_router])
    add_middleware(app=app)
    add_handle_exceptions(app=app)
    return app


app = create_app()
