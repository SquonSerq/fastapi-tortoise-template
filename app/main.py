import logging
import sys

from fastapi import FastAPI

from app.api.routes.router import grouping_router
from app.core import config
from app.core.events import create_start_app_handler, create_stop_app_handler

if config.SQL_DEBUG:
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)

    logger_db_client = logging.getLogger("tortoise.db_client")
    logger_db_client.setLevel(logging.DEBUG)
    logger_db_client.addHandler(sh)


def get_application() -> FastAPI:
    application = FastAPI(
        debug=config.DEBUG,
        title=config.PROJECT_NAME,
        summary="Project summary",
        description="Project description",
        version=config.VERSION,
        redirect_slashes=True,
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(grouping_router)

    return application


app = get_application()
