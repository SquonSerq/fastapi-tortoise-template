from app.core import config
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

# Tortoise init

TORTOISE_ORM = {
    "connections": {"default": config.DATABASE_URL},
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
        db_url=config.DATABASE_URL.unicode_string(),
        modules={"models": ["app.db.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
