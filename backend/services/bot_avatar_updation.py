import asyncio
from datetime import datetime, timezone, timedelta
from starlette.config import Config

from backend.models import Bot
from backend.utility.api_client import DiscordAPIClient


config = Config(".env")
api = DiscordAPIClient(authorization=f"Bot {config('BOT_TOKEN')}")


async def bot_avatar_updation_service(redis_conn):
    while True:
        now = datetime.now(timezone.utc)
        last_bot_updation = await redis_conn.get("BOT_AVATAR_UPDATION")
        last_updation_time = datetime.fromisoformat(last_bot_updation.decode('utf-8'))
        if (now - last_updation_time).total_seconds() > 43200:
            bots = await Bot.all()
            for bot in bots:
                bot_json = await api.get_bot_info(bot.id)
                if bot_json:
                    if bot.avatar != bot_json.get("avatar"):
                        bot.avatar = bot_json.get("avatar")
                        await bot.save()
                await asyncio.sleep(5)
            await redis_conn.set("BOT_AVATAR_UPDATION", str(now))
        await asyncio.sleep(3600)
