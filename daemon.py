while True:
    try:
        import sys
        import os
        import asyncio
        
        sys.path.insert(0, "D:/claw-агент")
        
        log = open("bot.log", "a")
        log.write(f"\n=== {asyncio.get_event_loop().time()} ===\n")
        
        from core.config import settings
        log.write(f"TG: {bool(settings.telegram_bot_token)}\n")
        
        from db.database import db
        log.write("DB OK\n")
        
        from bot.telegram import telegram_manager
        log.write("TG bot import OK\n")
        
        import main
        log.write("main import OK\n")
        
        log.write("Starting bot...\n")
        log.flush()
        
        asyncio.run(main.main())
        
        log.write("Done\n")
        log.close()
    except Exception as e:
        open("error.log", "a").write(str(e) + "\n")
    
    import time
    time.sleep(60)