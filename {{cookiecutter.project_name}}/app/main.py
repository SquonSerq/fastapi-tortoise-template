import logging
import sys

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes.router import grouping_router
from app.core import config
from app.core.events import create_start_app_handler, create_stop_app_handler

if config.SQL_DEBUG:
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)

    logger_db_client = logging.getLogger("tortoise.db_client")
    logger_db_client.setLevel(logging.DEBUG)
    logger_db_client.addHandler(sh)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_start_app_handler(app)
    yield
    create_stop_app_handler(app)


def get_application() -> FastAPI:
    application = FastAPI(
        debug=config.DEBUG,
        title="{{ cookiecutter.project_name }}",
        summary="{{ cookiecutter.project_summary }}",
        description="{{ cookiecutter.project_description }}",
        version=config.VERSION,
        redirect_slashes=True,
        lifespan=lifespan,
    )

    application.include_router(grouping_router)

    return application


app = get_application()
