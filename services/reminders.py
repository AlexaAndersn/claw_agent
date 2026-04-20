from datetime import datetime, timedelta
from typing import Callable, Awaitable
from core.config import settings


async def schedule_reminder(
    chat_id: str,
    title: str,
    trigger_time: datetime,
    send_func: Callable[[str, str], Awaitable[None]],
    t_minus_10: bool = True,
):
    now = datetime.now()
    
    if t_minus_10:
        t_minus_10_time = trigger_time - timedelta(minutes=10)
        if t_minus_10_time > now:
            delay = (t_minus_10_time - now).total_seconds()
            # Здесь должен быть вызов scheduler для отложенной задачи
            # Пока просто логируем
            print(f"T-10 reminder scheduled for {chat_id} at {t_minus_10_time}")

    if trigger_time > now:
        delay = (trigger_time - now).total_seconds()
        print(f"T-0 reminder scheduled for {chat_id} at {trigger_time}")


async def create_reminder(
    chat_id: str,
    title: str,
    minutes_from_now: int,
    callback: Callable[[str, str], Awaitable[None]],
) -> datetime:
    trigger_time = datetime.now() + timedelta(minutes=minutes_from_now)
    await schedule_reminder(chat_id, title, trigger_time, callback)
    return trigger_time