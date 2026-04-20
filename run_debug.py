#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, io, traceback

log_file = open(r"D:\claw-агент\debug.log", "w", encoding="utf-8")

def log(msg):
    log_file.write(msg + "\n")
    log_file.flush()

os.chdir(r"D:\claw-агент")
sys.path.insert(0, r"D:\claw-агент")

log("1. Starting...")

try:
    from core.config import settings
    log(f"2. Telegram: {bool(settings.telegram_bot_token)}")
    log(f"3. MAX: {bool(settings.max_bot_token)}")
except Exception as e:
    log(f"Config error: {e}")
    log_file.close()
    sys.exit(1)

log("4. Importing main...")

try:
    from main import main
    log("5. Running main()...")
    import asyncio
    asyncio.run(main())
    log("6. Done")
except Exception as e:
    log(f"Error: {e}")
    traceback.print_exc(file=log_file)

log_file.close()