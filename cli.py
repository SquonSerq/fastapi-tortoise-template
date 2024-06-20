import asyncio
import platform
import subprocess
import time
from enum import Enum
from functools import wraps
from pathlib import Path

import typer as typer
from aerich import Command
from tortoise import Tortoise

from app.db.setup import TORTOISE_ORM

app = typer.Typer()


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


class ProcessManager(str, Enum):
    uvicorn = "uvicorn"
    gunicorn = "gunicorn"


def get_migrations_path() -> Path:
    return (Path(__file__).parent / "app/migrations").absolute()


async def init_aerich() -> Command:
    command = Command(
        tortoise_config=TORTOISE_ORM, app="models", location=get_migrations_path()
    )
    await command.init()
    return command


class tortoise_ctx(object):
    async def __aenter__(self):
        await Tortoise.init(config=TORTOISE_ORM)

    async def __aexit__(self, type, value, traceback):
        await Tortoise.close_connections()

@app.command()
@coro
async def init_db():
    command = await init_aerich()
    try:
        output = await command.init_db(safe=True)
        print(output)
    except FileExistsError:
        print("Init was already done")


@app.command()
@coro
async def make_migrations(message: str = "update"):
    command = await init_aerich()
    output = await command.migrate(message)
    print(f"Created migration: {output}")


@app.command()
@coro
async def migrate():
    command = await init_aerich()
    migrations = await command.upgrade(run_in_transaction=True)
    if not migrations:
        print("No new migrations were applied.")
        return
    output_migrations_str = "\n".join(["\n", *migrations])
    print(f"Successfully migrated: {output_migrations_str}")


if __name__ == "__main__":
    app()
