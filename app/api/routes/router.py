from fastapi import APIRouter

from app.api.routes.v1.router import v1_router
from app.core import config

grouping_router = APIRouter()

grouping_router.include_router(v1_router, prefix=config.API_ROUTE)
