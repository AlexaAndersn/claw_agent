import asyncio
import logging
import sys
from contextlib import suppress

sys.stdout.reconfigure(line_buffering=True, encoding='utf-8')
sys.stderr.reconfigure(line_buffering=True, encoding='utf-8')

print("=== Claw-Agent Starting ===", flush=True)

from bot.telegram import telegram_manager
from bot.max import max_manager
from bot.handlers import register_telegram_handlers
from db.database import db
from core.scheduler import scheduler
from core.config import settings
from jobs.morning import send_morning_greeting
from jobs.night import send_night_greeting

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def init_database():
    try:
        await db.init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database init error: {e}")


async def init_bots():
    try:
        tg = await telegram_manager.init()
        if tg:
            register_telegram_handlers(telegram_manager.dp)
            logger.info("Telegram bot initialized")
    except Exception as e:
        logger.error(f"Telegram bot init error: {e}")

    try:
        mx = await max_manager.init()
        if mx and settings.max_webhook_url:
            await max_manager.set_webhook(settings.max_webhook_url)
            logger.info(f"MAX webhook set: {settings.max_webhook_url}")
        elif mx:
            logger.info("MAX bot initialized (no webhook URL)")
    except Exception as e:
        logger.error(f"MAX bot init error: {e}")


async def init_scheduler():
    try:
        await scheduler.start()

        scheduler.add_cron_job(
            send_morning_greeting,
            "morning_greeting",
            settings.morning_hour,
            settings.morning_minute,
            jitter=True,
        )

        scheduler.add_cron_job(
            send_night_greeting,
            "night_greeting",
            settings.night_hour,
            settings.night_minute,
            jitter=True,
        )

        logger.info("Scheduler initialized with jobs")
    except Exception as e:
        logger.error(f"Scheduler init error: {e}")


async def run_telegram_polling():
    if telegram_manager.bot and telegram_manager.dp:
        logger.info("Starting Telegram polling...")
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                await telegram_manager.dp.start_polling(telegram_manager.bot)
                break
            except Exception as e:
                retry_count += 1
                logger.error(f"Polling error (attempt {retry_count}): {e}")
                if retry_count < max_retries:
                    await asyncio.sleep(5)
                else:
                    logger.error("Max retries reached, stopping polling")


async def main():
    print("=== Claw-Agent Starting ===", flush=True)
    print(f"Telegram: {bool(settings.telegram_bot_token)}", flush=True)
    print(f"MAX: {bool(settings.max_bot_token)}", flush=True)
    logger.info("Starting Claw-Agent...")

    await init_database()
    await init_bots()
    await init_scheduler()

    if telegram_manager.bot and telegram_manager.dp:
        try:
            await run_telegram_polling()
        except Exception as e:
            logger.error(f"Polling error: {e}")
    else:
        logger.info("No Telegram bot configured, running scheduler only")
        while True:
            await asyncio.sleep(3600)


async def shutdown():
    logger.info("Shutting down...")
    await scheduler.stop()
    await telegram_manager.close()
    await max_manager.close()
    await db.close()
    logger.info("Shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Press Ctrl+C to exit...")
        input()