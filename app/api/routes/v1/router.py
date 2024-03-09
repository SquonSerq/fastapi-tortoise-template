from fastapi import APIRouter

from .example_routes import router as example_routes

v1_router = APIRouter()

v1_router.include_router(example_routes, tags=["example"], prefix="/example")
