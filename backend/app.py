import debugpy
from fastapi.responses import JSONResponse
from fastapi import status, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from backend.auctions import auctions_router
from backend.shared import GeneralAPIException
from backend.container import ApplicationContainer

container = ApplicationContainer()

container.check_dependencies()
container.reset_singletons()

logger = container.logging_logger()


def attach_debug():
    debug_host = "0.0.0.0"
    debug_port = 9500
    debugpy.listen((debug_host, debug_port))
    logger.info(message=f'DEBUG Attached!, running in: {debug_host}:{debug_port}')


def attach_test_debug_waiting_connection():
    debug_host = "0.0.0.0"
    debug_port = 9500
    debugpy.listen((debug_host, debug_port))
    logger.info(message='Waiting for DEBUG attaching')
    debugpy.wait_for_client()
    logger.info(message=f'DEBUG Attached!, running in: {debug_host}:{debug_port}')


def add_routers(*, app: FastAPI, routers: list[APIRouter]) -> None:
    for router in routers:
        app.include_router(router=router, prefix="/v1")


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


def add_startup_events(app, databases_to_init, caches_to_init):
    @app.on_event("startup")
    async def startup() -> None:
        for db_to_init in databases_to_init:
            db_to_init.create_database()
        logger.info(message="Database started sucessfull!")

        for cache_to_init in caches_to_init:
            cache_to_init.init_cache()
        logger.info(message="Caches started sucessfull!")


def add_shutdown_events(app, caches_to_close):
    @app.on_event("shutdown")
    async def shutdown() -> None:
        for cache_to_close in caches_to_close:
            await cache_to_close.close_cache()

        logger.info(message="Caches closed sucessfull!")


def create_app() -> FastAPI:
    # attach_test_debug_waiting_connection()
    # attach_debug()
    app = FastAPI()

    add_dependency_injection(app=app, container=container)

    add_startup_events(
        app=app,
        databases_to_init=[container.auctions_repository()],
        caches_to_init=[container.fastapi_redis_cache()],
    )

    add_shutdown_events(app=app, caches_to_close=[container.fastapi_redis_cache()])

    add_routers(app=app, routers=[auctions_router])

    add_middleware(app=app)

    add_handle_exceptions(app=app)

    return app


app = create_app()
