#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os

print("=== Bot Debug ===")

try:
    os.chdir("D:/claw-агент")
    sys.path.insert(0, "D:/claw-агент")
    
    print("1. Importing config...")
    from core.config import settings
    print(f"   TG: {'OK' if settings.telegram_bot_token else 'MISSING'}")
    
    print("2. Importing database...")
    from db.database import db
    print("   DB: OK")
    
    print("3. Importing bots...")
    from bot.telegram import telegram_manager
    from bot.max import max_manager
    print("   Bots: OK")
    
    print("4. Importing main...")
    import main
    print("   Main: OK")
    
    print("=== All OK ===")
    print("Run: py main.py")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

input("\nPress Enter to exit...")