from datetime import datetime
from bot.telegram import telegram_manager
from bot.max import max_manager
from db.repository import account_repo, message_log_repo, user_repo
from services.weather import get_weather_text
from core.config import settings


async def send_morning_greeting():
    accounts = await account_repo.get_all()

    for account in accounts:
        chat_id = account.chat_id
        
        user = await user_repo.get_by_chat_id(chat_id)
        city = user.city if user and user.city else settings.default_city
        
        weather_text = await get_weather_text(city)

        message = (
            f"🌅 Доброе утро!\n\n"
            f"Погода в {city}: {weather_text}\n\n"
            f"Хорошего дня! ☀️"
        )

        try:
            if account.platform == "telegram" and telegram_manager.bot:
                await telegram_manager.bot.send_message(chat_id, message)
            elif account.platform == "max":
                await max_manager.send_message(chat_id, message)

            await message_log_repo.log("morning", chat_id, message)
        except Exception as e:
            print(f"Failed to send morning message to {chat_id}: {e}")