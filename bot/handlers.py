from datetime import datetime, timedelta
from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards import (
    get_main_keyboard,
    get_settings_keyboard,
    get_schedule_keyboard,
    get_cancel_keyboard,
    get_settings_cancel_keyboard,
    get_schedule_cancel_keyboard,
)
from core.security import security
from core.config import settings
from db.repository import user_repo, account_repo, reminder_repo
from bot.telegram import telegram_manager
from bot.max import max_manager


class UserSettings(StatesGroup):
    waiting_for_city = State()
    waiting_for_timezone = State()
    waiting_for_morning_time = State()
    waiting_for_night_time = State()
    waiting_for_plan = State()
    waiting_for_reminder_title = State()
    waiting_for_reminder_time = State()


async def cmd_start(message: types.Message):
    if not security.check_access(message.chat.id):
        return

    user = await user_repo.get_or_create(
        str(message.chat.id), message.from_user.full_name
    )

    text = (
        "👋 Привет! Я Claw-Agent.\n\n"
        f"📍 Город: {user.city}\n"
        f"🌍 Часовой пояс: {user.timezone}\n\n"
        "🌅 Утро: {:02d}:{:02d}\n"
        "🌙 Вечер: {:02d}:{:02d}\n\n"
        "Выбери действие:".format(
            settings.morning_hour, settings.morning_minute,
            settings.night_hour, settings.night_minute
        )
    )
    await message.answer(text, reply_markup=get_main_keyboard())


async def cmd_help(message: types.Message):
    if not security.check_access(message.chat.id):
        return

    text = (
        "📖 Доступные команды:\n\n"
        "/start - Запустить бота\n"
        "/help - Показать справку\n"
        "/status - Статус бота\n"
        "/settings - Настройки\n"
        "/schedule - Расписание\n"
        "/stats - Статистика"
    )
    await message.answer(text)


async def cmd_status(message: types.Message):
    if not security.check_access(message.chat.id):
        return

    accounts = await account_repo.get_all()
    text = f"✅ Claw-Agent работает\n\n📱 Активных аккаунтов: {len(accounts)}"
    await message.answer(text)


async def cmd_settings(message: types.Message):
    if not security.check_access(message.chat.id):
        return

    await message.answer(
        "⚙️ Настройки", reply_markup=get_settings_keyboard()
    )


async def cmd_schedule(message: types.Message):
    if not security.check_access(message.chat.id):
        return

    await message.answer(
        f"📋 Расписание\n\n"
        f"🌅 Утро: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n"
        f"🌙 Вечер: {settings.night_hour:02d}:{settings.night_minute:02d}",
        reply_markup=get_schedule_keyboard()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())


async def handle_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data
    chat_id = str(callback.from_user.id)

    user = await user_repo.get_by_chat_id(chat_id)
    city = user.city if user else "Казань"
    timezone = user.timezone if user else "Europe/Moscow"

    if data == "stats":
        accounts = await account_repo.get_all()
        await callback.message.edit_text(
            f"📊 Статистика\n\n"
            f"👥 Пользователей: {len(accounts)}\n"
            f"📍 Город: {city}\n"
            f"🌍 Часовой пояс: {timezone}\n\n"
            f"🌅 Утро: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n"
            f"🌙 Вечер: {settings.night_hour:02d}:{settings.night_minute:02d}",
            reply_markup=get_main_keyboard()
        )
    elif data == "settings":
        await callback.message.edit_text(
            f"⚙️ Текущие настройки:\n\n"
            f"📍 Город: {city}\n"
            f"🌍 Часовой пояс: {timezone}",
            reply_markup=get_settings_keyboard()
        )
    elif data == "schedule":
        await callback.message.edit_text(
            f"📋 Расписание\n\n"
            f"🌅 Утро: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n"
            f"🌙 Вечер: {settings.night_hour:02d}:{settings.night_minute:02d}\n\n"
            f"Нажмите на кнопку для настройки",
            reply_markup=get_schedule_keyboard()
        )
    elif data == "add_reminder":
        await state.set_state(UserSettings.waiting_for_reminder_title)
        await callback.message.edit_text(
            "⏰ Новое напоминание\n\n"
            "Введи название события:\n"
            "Например: \"Встреча с клиентом\"",
            reply_markup=get_cancel_keyboard()
        )
    elif data == "back":
        await state.clear()
        user = await user_repo.get_by_chat_id(chat_id)
        city = user.city if user else "Казань"
        timezone = user.timezone if user else "Europe/Moscow"
        await callback.message.edit_text(
            f"👋 Главное меню\n\n"
            f"📍 Город: {city}\n"
            f"🌍 Часовой пояс: {timezone}\n\n"
            f"🌅 Утро: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n"
            f"🌙 Вечер: {settings.night_hour:02d}:{settings.night_minute:02d}",
            reply_markup=get_main_keyboard()
        )
    elif data == "cancel":
        await state.clear()
        await callback.message.edit_text(
            "Отменено. Нажмите /start",
            reply_markup=get_main_keyboard()
        )
    elif data == "back_to_menu":
        await state.clear()
        user = await user_repo.get_by_chat_id(chat_id)
        city = user.city if user else "Казань"
        timezone = user.timezone if user else "Europe/Moscow"
        await callback.message.edit_text(
            f"👋 Главное меню\n\n"
            f"📍 Город: {city}\n"
            f"🌍 Часовой пояс: {timezone}\n\n"
            f"🌅 Утро: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n"
            f"🌙 Вечер: {settings.night_hour:02d}:{settings.night_minute:02d}",
            reply_markup=get_main_keyboard()
        )
    elif data == "back_to_settings":
        await state.clear()
        user = await user_repo.get_by_chat_id(chat_id)
        city = user.city if user else "Казань"
        timezone = user.timezone if user else "Europe/Moscow"
        await callback.message.edit_text(
            f"⚙️ Текущие настройки:\n\n"
            f"📍 Город: {city}\n"
            f"🌍 Часовой пояс: {timezone}",
            reply_markup=get_settings_keyboard()
        )
    elif data == "back_to_schedule":
        await state.clear()
        await callback.message.edit_text(
            f"📋 Расписание\n\n"
            f"🌅 Утро: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n"
            f"🌙 Вечер: {settings.night_hour:02d}:{settings.night_minute:02d}\n\n"
            f"Нажмите на кнопку для настройки",
            reply_markup=get_schedule_keyboard()
        )
    elif data == "set_plan":
        user = await user_repo.get_by_chat_id(chat_id)
        current_plan = user.plan_for_tomorrow if user and user.plan_for_tomorrow else "Не задано"
        await callback.message.edit_text(
            f"📝 Планы на завтра\n\n"
            f"Текущий план: {current_plan}\n\n"
            "Введите ваши планы на завтра\n(каждый пункт с новой строки, начинайте с • или -)\n\n"
            "Например:\nВстреча с другом\nСходить в магазин\nПрочитать книгу",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(UserSettings.waiting_for_plan)
    elif data == "set_city":
        await callback.message.edit_text(
            "🌤 Введите название города для погоды:\n"
            "Например: Москва, Казань, Санкт-Петербург\n\n"
            "Нажмите 'Назад' для возврата",
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(UserSettings.waiting_for_city)
    elif data == "set_timezone":
        await callback.message.edit_text(
            "🌍 Введите часовой пояс:\n"
            "Например: Europe/Moscow, Asia/Yekaterinburg\n\n"
            "Нажмите 'Назад' для возврата",
            reply_markup=get_settings_cancel_keyboard()
        )
        await state.set_state(UserSettings.waiting_for_timezone)
    elif data == "set_morning":
        await callback.message.edit_text(
            "🌅 Утреннее сообщение\n\n"
            f"Текущее время: {settings.morning_hour:02d}:{settings.morning_minute:02d}\n\n"
            "Введите время в формате ЧЧ:ММ\n"
            "Например: 08:00\n\n"
            "Нажмите 'Назад' для возврата",
            reply_markup=get_schedule_cancel_keyboard()
        )
        await state.set_state(UserSettings.waiting_for_morning_time)
    elif data == "set_night":
        await callback.message.edit_text(
            "🌙 Вечернее сообщение\n\n"
            f"Текущее время: {settings.night_hour:02d}:{settings.night_minute:02d}\n\n"
            "Введите время в формате ЧЧ:ММ\n"
            "Например: 23:00\n\n"
            "Нажмите 'Назад' для возврата",
            reply_markup=get_schedule_cancel_keyboard()
        )
        await state.set_state(UserSettings.waiting_for_night_time)


async def handle_city_input(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена" or message.text == "Отмена" or message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    city = message.text.strip()
    await user_repo.update_settings(str(message.chat.id), city=city)
    await message.answer(
        f"🌤 Город установлен: {city}",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


async def handle_timezone_input(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена" or message.text == "Отмена" or message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    timezone = message.text.strip()
    await user_repo.update_settings(str(message.chat.id), timezone=timezone)
    await message.answer(
        f"🌍 Часовой пояс установлен: {timezone}",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


async def handle_morning_time_input(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена" or message.text == "Отмена" or message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    time_str = message.text.strip()
    try:
        parts = time_str.split(":")
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            settings.morning_hour = hour
            settings.morning_minute = minute
            await message.answer(
                f"🌅 Утреннее время установлено: {hour:02d}:{minute:02d}",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer("Неверное время. Введите в формате ЧЧ:ММ")
    except:
        await message.answer("Неверный формат. Введите в формате ЧЧ:ММ")
    await state.clear()


async def handle_night_time_input(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена" or message.text == "Отмена" or message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    time_str = message.text.strip()
    try:
        parts = time_str.split(":")
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 else 0
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            settings.night_hour = hour
            settings.night_minute = minute
            await message.answer(
                f"🌙 Вечернее время установлено: {hour:02d}:{minute:02d}",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer("Неверное время. Введите в формате ЧЧ:ММ")
    except:
        await message.answer("Неверный формат. Введите в формате ЧЧ:ММ")
    await state.clear()


async def handle_plan_input(message: types.Message, state: FSMContext):
    if message.text == "❌ Отмена" or message.text == "Отмена" or message.text == "🔙 Назад":
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    plan = message.text.strip()
    await user_repo.update_settings(str(message.chat.id), plan=plan)
    
    plan_lines = [line.strip() for line in plan.split('\n') if line.strip()]
    plan_formatted = '\n'.join([f"• {line.lstrip('•- ')}" for line in plan_lines])
    
    await message.answer(
        f"📝 Планы на завтра сохранены:\n\n{plan_formatted}",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


async def handle_reminder_title(message: types.Message, state: FSMContext):
    if message.text in ["❌ Отмена", "Отмена", "🔙 Назад"]:
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    title = message.text.strip()
    await state.update_data(reminder_title=title)
    await state.set_state(UserSettings.waiting_for_reminder_time)
    await message.answer(
        f"⏰ Напоминание: {title}\n\n"
        "Введите время события в формате ЧЧ:ММ сегодня или завтра\n"
        "Например: 15:00 или завтра 14:30",
        reply_markup=get_cancel_keyboard()
    )


async def handle_reminder_time(message: types.Message, state: FSMContext):
    if message.text in ["❌ Отмена", "Отмена", "🔙 Назад"]:
        await state.clear()
        await message.answer("Отменено. Нажмите /start", reply_markup=get_main_keyboard())
        return
    
    text = message.text.strip().lower()
    chat_id = str(message.chat.id)
    
    now = datetime.now()
    is_tomorrow = "завтра" in text
    time_str = text.replace("завтра", "").strip()
    
    try:
        hour, minute = map(int, time_str.split(":"))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError()
    except:
        await message.answer(
            "❌ Неверный формат. Введите время в формате ЧЧ:ММ\n"
            "Например: 15:00",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    event_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if is_tomorrow or event_time < now:
        if event_time < now:
            event_time += timedelta(days=1)
    
    data = await state.get_data()
    title = data.get("reminder_title", "Событие")
    
    minutes_before_values = [10, 5, 0]
    for mins in minutes_before_values:
        remind_at = event_time - timedelta(minutes=mins) if mins > 0 else event_time
        await reminder_repo.create(chat_id, title, remind_at, mins)
    
    await message.answer(
        f"✅ Напоминание создано!\n\n"
        f"Событие: {title}\n"
        f"Время: {event_time.strftime('%H:%M')}\n\n"
        f"Вы получите напоминания за 10 мин, 5 мин и в момент события.",
        reply_markup=get_main_keyboard()
    )
    await state.clear()


def register_telegram_handlers(dp):
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_help, Command(commands=["help"]))
    dp.message.register(cmd_status, Command(commands=["status"]))
    dp.message.register(cmd_settings, Command(commands=["settings"]))
    dp.message.register(cmd_schedule, Command(commands=["schedule"]))
    dp.message.register(cmd_cancel, Command(commands=["cancel", "отмена"]))
    dp.message.register(handle_city_input, UserSettings.waiting_for_city)
    dp.message.register(handle_timezone_input, UserSettings.waiting_for_timezone)
    dp.message.register(handle_morning_time_input, UserSettings.waiting_for_morning_time)
    dp.message.register(handle_night_time_input, UserSettings.waiting_for_night_time)
    dp.message.register(handle_plan_input, UserSettings.waiting_for_plan)
    dp.message.register(handle_reminder_title, UserSettings.waiting_for_reminder_title)
    dp.message.register(handle_reminder_time, UserSettings.waiting_for_reminder_time)
    dp.callback_query.register(handle_callback)


def setup_filters(dp):
    pass


async def handle_max_command(chat_id: str, command: str, text: str = None):
    if not security.check_access(int(chat_id)):
        return

    await user_repo.get_or_create(chat_id)

    if command == "/start":
        msg = (
            "👋 Привет! Я Claw-Agent.\n\n"
            "Я помогу тебе с:\n"
            "• Утренними и вечерними сообщениями\n"
            "• Напоминаниями о делах\n"
            "• Погодой и планированием\n\n"
            "Выбери действие:"
        )
        await max_manager.send_message(chat_id, msg)
    elif command == "/help":
        msg = (
            "📖 Доступные команды:\n\n"
            "/start - Запустить бота\n"
            "/help - Показать справку\n"
            "/status - Статус бота\n"
            "/settings - Настройки"
        )
        await max_manager.send_message(chat_id, msg)
    elif command == "/status":
        accounts = await account_repo.get_all()
        msg = f"✅ Claw-Agent работает\n\n📱 Активных аккаунтов: {len(accounts)}"
        await max_manager.send_message(chat_id, msg)