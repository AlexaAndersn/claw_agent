# -*- coding: utf-8 -*-
import sys, os, logging

logging.basicConfig(
    filename="D:/claw-агент/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)
log.info("=== Starting Bot ===")

try:
    os.chdir("D:/claw-агент")
    sys.path.insert(0, "D:/claw-агент")
    
    from core.config import settings
    log.info(f"Config loaded, TG: {bool(settings.telegram_bot_token)}")
    
    from db.database import db
    log.info("Database imported")
    
    from bot.telegram import telegram_manager
    from bot.max import max_manager
    log.info("Bots imported")
    
    import main
    log.info("Main imported")
    
    import asyncio
    asyncio.run(main.main())
    
except Exception as e:
    log.error(f"Error: {e}")
    
finally:
    log.info("Bot stopped")
    input("Press Enter to exit...")