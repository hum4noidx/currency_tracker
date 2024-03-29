from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
from app.services.courses_updater import update_courses


def create_app():
    description = f"{settings.PROJECT_NAME} API"
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PATH}/openapi.json",
        docs_url="/docs/",
        description=description,
        redoc_url="/redoc",
    )
    setup_routers(app)
    setup_cors_middleware(app)
    scheduler = AsyncIOScheduler()
    setup_jobs(scheduler)
    scheduler.start()
    return app


def setup_jobs(scheduler: AsyncIOScheduler) -> None:
    scheduler.add_job(
        update_courses,
        trigger="interval",
        seconds=5,
        id="update_courses",
        name="Update courses",
    )


def setup_routers(app: FastAPI) -> None:
    app.include_router(api_router, prefix=settings.API_PATH)
    use_route_names_as_operation_ids(app)


def setup_cors_middleware(app):
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    route_names = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in route_names:
                raise Exception("Route function names should be unique")
            route.operation_id = route.name
            route_names.add(route.name)
