import asyncio
from datetime import datetime, timezone
from starlette.config import Config

from backend.models import Server
from backend.utility.api_client import DiscordAPIClient


config = Config(".env")
api = DiscordAPIClient(authorization=f"Bot {config('BOT_TOKEN')}")


async def guild_icon_updation_service(redis_conn):
    while True:
        now = datetime.now(timezone.utc)
        last_guild_updation = await redis_conn.get("GUILD_ICON_UPDATION")
        last_updation_time = datetime.fromisoformat(last_guild_updation.decode('utf-8'))

        if (now - last_updation_time).total_seconds() > 43200:
            guilds = await Server.all()

            for guild in guilds:
                guild_json = await api.get_bot_info(guild.id)
                if guild.icon != guild_json.get("icon"):
                    guild.icon = guild_json.get("icon")
                    await guild.save()
                await asyncio.sleep(5)
        await asyncio.sleep(3600)
