import json
import httpx
from starlette.config import Config

config = Config(".env")
url = "https://discord.com/api/v9"


class DiscordAPIClient:
    headers = {"Content-Type": "application/json"}
    session = None
    client_id = config("DISCORD_CLIENT_ID")
    client_secret = config("DISCORD_CLIENT_SECRET")

    def __init__(self, authorization):
        self.headers["Authorization"] = authorization
        self.session = httpx.AsyncClient(headers=self.headers)

    async def get(self, endpoint):
        async with self.session as session:
            try:
                resp = await session.get(url+endpoint)
                return resp.json()
            except httpx.ConnectTimeout:
                return
            except httpx.TimeoutException:
                return
            finally:
                await self.close()

    async def post(self, endpoint, data):
        async with self.session as session:
            try:
                resp = await session.post(url+endpoint, data=data)
                return resp.json()
            except httpx.ConnectTimeout:
                return
            except httpx.TimeoutException:
                return
            finally:
                await self.close()

    async def refresh_access_token(self, refresh_token):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        return await self.post("/oauth2/token", data=payload)

    async def get_bot_info(self, bot_id):
        return await self.get(f"/users/{bot_id}")

    async def get_guild_info(self, guild_id):
        return await self.get(f"/guilds/{guild_id}")

    async def close(self):
        await self.session.aclose()
