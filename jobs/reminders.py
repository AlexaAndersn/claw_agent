from bot.telegram import telegram_manager
from bot.max import max_manager
from db.repository import reminder_repo, message_log_repo


async def check_reminders():
    pending = await reminder_repo.get_pending()

    for reminder in pending:
        if reminder.minutes_before > 0:
            text = f"⏰ Напоминание: {reminder.title}\nЧерез {reminder.minutes_before} мин."
        else:
            text = f"🔔 Сейчас: {reminder.title}"

        try:
            if telegram_manager.bot:
                await telegram_manager.bot.send_message(reminder.chat_id, text)
            
            await reminder_repo.mark_sent(reminder.id)
            await message_log_repo.log("reminder", reminder.chat_id, text)
        except Exception as e:
            print(f"Failed to send reminder to {reminder.chat_id}: {e}")