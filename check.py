# test import
import sys, os
sys.path.insert(0, "D:/claw-агент")

print("1. Starting...")
print("2. Importing config...")

from core.config import settings
print("3. Config imported")

print(f"TG: {bool(settings.telegram_bot_token)}")
print(f"MAX: {bool(settings.max_bot_token)}")
print(f"Weather: {bool(settings.yandex_weather_api_key)}")

print("4. All done")