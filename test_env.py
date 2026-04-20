import sys
import os

# Добавить текущую директорию в путь
os.chdir(r"D:\claw-агент")
sys.path.insert(0, r"D:\claw-агент")

try:
    print("Starting import...")
    from core.config import settings
    print(f"Config loaded. Telegram token: {'set' if settings.telegram_bot_token else 'empty'}")
    
    from db.database import db
    print("Database import OK")
    
    print("All imports OK")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")