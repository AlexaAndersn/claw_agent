from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import settings


class TelegramBotManager:
    def __init__(self):
        self.bot: Bot = None
        self.dp: Dispatcher = None

    async def init(self):
        if not settings.telegram_bot_token:
            return None

        self.bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        return self.bot, self.dp

    async def close(self):
        if self.bot:
            await self.bot.session.close()


telegram_manager = TelegramBotManager()