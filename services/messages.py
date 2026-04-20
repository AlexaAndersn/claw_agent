from core.config import settings
from services.weather import get_weather_text


async def get_morning_message(city: str = None) -> str:
    city = city or settings.default_city
    weather = await get_weather_text(city)

    return (
        f"🌅 Доброе утро!\n\n"
        f"Погода в {city}: {weather}\n\n"
        f"Хорошего дня! ☀️"
    )


async def get_night_message(city: str = None) -> str:
    city = city or settings.default_city
    weather = await get_weather_text(city)

    return (
        f"🌙 Спокойной ночи!\n\n"
        f"Погода на завтра: {weather}\n\n"
        f"Планы на завтра:\n"
        f"• ------- \n"
        f"• -------\n\n"
        f"Сладких снов! 💤"
    )


async def get_reminder_message(title: str, minutes: int) -> str:
    if minutes > 0:
        time_text = f"Через {minutes} минут"
    else:
        time_text = "Сейчас"

    return f"⏰ Напоминание: {title}\n\n{time_text}!"


async def get_custom_message(text: str) -> str:
    return text