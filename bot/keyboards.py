from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
            [InlineKeyboardButton(text="📋 Расписание", callback_data="schedule")],
            [InlineKeyboardButton(text="⏰ Напоминание", callback_data="add_reminder")],
            [InlineKeyboardButton(text="📝 Планы на завтра", callback_data="set_plan")],
        ]
    )


def get_settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Часовой пояс", callback_data="set_timezone")],
            [InlineKeyboardButton(text="🌤 Город", callback_data="set_city")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")],
        ]
    )


def get_schedule_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌅 Изменить утро", callback_data="set_morning")],
            [InlineKeyboardButton(text="🌙 Изменить вечер", callback_data="set_night")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")],
        ]
    )


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )


def get_settings_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )


def get_schedule_cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_schedule")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")],
        ]
    )