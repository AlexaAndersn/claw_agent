#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

# Изменить кодировку вывода
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

os.chdir(r"D:\claw-агент")
sys.path.insert(0, r"D:\claw-агент")

print("=== Starting ===", flush=True)

try:
    from core.config import settings
    print(f"Telegram: {bool(settings.telegram_bot_token)}", flush=True)
    print(f"MAX: {bool(settings.max_bot_token)}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
    sys.exit(1)

try:
    from main import main
    print("Main imported OK", flush=True)
    import asyncio
    asyncio.run(main())
except Exception as e:
    print(f"Error: {e}", flush=True)
    import traceback
    traceback.print_exc()