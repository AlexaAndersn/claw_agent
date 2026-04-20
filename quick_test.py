#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
os.chdir(r"D:\claw-агент")
sys.path.insert(0, r"D:\claw-агент")

log = open(r"D:\claw-агент\log.txt", "w", encoding="utf-8")

try:
    log.write("Loading config...\n")
    from core.config import settings
    log.write(f"Telegram: {'OK' if settings.telegram_bot_token else 'MISSING'}\n")
    log.write(f"MAX: {'OK' if settings.max_bot_token else 'MISSING'}\n")
    log.write(f"Weather: {'OK' if settings.yandex_weather_api_key else 'MISSING'}\n")
except Exception as e:
    log.write(f"Config error: {e}\n")

try:
    log.write("Loading database...\n")
    from db.database import db
    log.write("Database OK\n")
except Exception as e:
    log.write(f"Database error: {e}\n")

log.write("Done\n")
log.close()