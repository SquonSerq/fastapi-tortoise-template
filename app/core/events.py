from typing import Callable

from fastapi import FastAPI

from app.db.setup import init_db_tortoise


def create_start_app_handler(app: FastAPI, **kwargs) -> Callable:
    async def start_app() -> None:
        await init_db_tortoise(app)

    return start_app


def create_stop_app_handler(app: FastAPI, **kwargs) -> Callable:
    async def stop_app() -> None:
        pass

    return stop_app
