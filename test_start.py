import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("D:/claw-агент/bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

logger.info("=== Claw-Agent Starting ===")

try:
    from core.config import settings
    logger.info(f"Telegram token: {'OK' if settings.telegram_bot_token else 'MISSING'}")
    logger.info(f"MAX token: {'OK' if settings.max_bot_token else 'MISSING'}")
    logger.info(f"Weather API: {'OK' if settings.yandex_weather_api_key else 'MISSING'}")
except Exception as e:
    logger.error(f"Config error: {e}")

logger.info("Config loaded")

try:
    from db.database import db
    logger.info("Database module OK")
except Exception as e:
    logger.error(f"Database error: {e}")

logger.info("=== Ready ===")