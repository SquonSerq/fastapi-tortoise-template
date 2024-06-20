from app.core import config
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# Tortoise init

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": config.POSTGRES_SERVER,
                "port": config.POSTGRES_PORT,
                "user": config.POSTGRES_USER,
                "password": config.POSTGRES_PASSWORD,
                "database": config.POSTGRES_DB,
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


async def init_db_tortoise(application: FastAPI):
    register_tortoise(
        application,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
