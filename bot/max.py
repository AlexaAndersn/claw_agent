import httpx
from core.config import settings


class MaxBotManager:
    def __init__(self):
        self.base_url = "https://api.max.ru/bot/v1"
        self.token = settings.max_bot_token
        self.client = None

    async def init(self):
        if not self.token:
            return None
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=30.0,
        )
        return self.client

    async def close(self):
        if self.client:
            await self.client.aclose()

    async def send_message(self, chat_id: str, text: str, keyboard: dict = None):
        if not self.client:
            return None

        payload = {"chat_id": chat_id, "text": text}
        if keyboard:
            payload["reply_markup"] = keyboard

        response = await self.client.post("/sendMessage", json=payload)
        return response.json()

    async def get_me(self):
        if not self.client:
            return None
        response = await self.client.post("/getMe")
        return response.json()

    async def set_webhook(self, url: str):
        if not self.client:
            return None
        response = await self.client.post(
            "/setWebhook", json={"url": url}
        )
        return response.json()


max_manager = MaxBotManager()