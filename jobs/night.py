from bot.telegram import telegram_manager
from bot.max import max_manager
from db.repository import account_repo, message_log_repo, user_repo
from services.weather import get_weather_text
from core.config import settings


async def send_night_greeting():
    accounts = await account_repo.get_all()

    for account in accounts:
        chat_id = account.chat_id
        
        user = await user_repo.get_by_chat_id(chat_id)
        city = user.city if user and user.city else settings.default_city
        plan = user.plan_for_tomorrow if user and user.plan_for_tomorrow else "Не запланировано"
        
        weather_text = await get_weather_text(city)

        message = (
            f"🌙 Спокойной ночи!\n\n"
            f"Погода на завтра в {city}: {weather_text}\n\n"
            f"📝 Планы на завтра:\n{plan}\n\n"
            f"Сладких снов! 💤"
        )

        try:
            if account.platform == "telegram" and telegram_manager.bot:
                await telegram_manager.bot.send_message(chat_id, message)
            elif account.platform == "max":
                await max_manager.send_message(chat_id, message)

            await message_log_repo.log("night", chat_id, message)
            
            await user_repo.update_settings(chat_id, plan="")
            
        except Exception as e:
            print(f"Failed to send night message to {chat_id}: {e}")