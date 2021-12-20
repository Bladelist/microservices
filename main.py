
import asyncio
import aioredis
from uvicorn.main import run
from tortoise.contrib.starlette import register_tortoise

from starlette.applications import Starlette
from starlette.config import Config
from backend.services.bot_avatar_updation import bot_avatar_updation_service
from backend.services.server_icon_updation import guild_icon_updation_service

config = Config('.env')
DEBUG = config('DEBUG', cast=bool, default=False)
host = "0.0.0.0"
port = 8000
redis_conn = None
if DEBUG:
    host = "127.0.0.1"
    port = 7000

app = Starlette(debug=DEBUG)
register_tortoise(
    app,
    db_url=config("DB_URI"),
    modules={"models": ["backend.models"]},
    generate_schemas=False
)


@app.on_event('startup')
async def startup():
    global redis_conn
    redis_conn = await aioredis.from_url(url=config("REDIS_URI"), username="default", password=config("REDIS_PASSWORD"))


@app.on_event("startup")
async def run_tasks():
    loop = asyncio.get_event_loop()
    loop.create_task(bot_avatar_updation_service(redis_conn))
    # loop.create_task(guild_icon_updation_service(redis_conn))


if __name__ == "__main__":
    run("main:app", reload=True, host=host, port=port, forwarded_allow_ips='*', proxy_headers=True)
