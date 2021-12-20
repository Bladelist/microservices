import asyncio
from backend.models import Bot


async def bot_avatar_updation_service():
    while True:
        bots = await Bot.all()
        for bot in bots:
            print(
                bot.avatar
            )
        await asyncio.sleep(1900)
