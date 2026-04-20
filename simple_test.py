log = open("test_run.log", "w")
log.write("started\n")
log.flush()

import sys, os
log.write(f"cwd: {os.getcwd()}\n")
log.flush()

sys.path.insert(0, "D:/claw-агент")
log.write("path added\n")
log.flush()

log.write("importing config...\n")
log.flush()
from core.config import settings
log.write(f"config ok, telegram: {bool(settings.telegram_bot_token)}\n")
log.flush()

log.write("importing db...\n")
log.flush()
from db.database import db
log.write("db ok\n")
log.flush()

log.write("importing bots...\n")
log.flush()
from bot.telegram import telegram_manager
from bot.max import max_manager
log.write("bots imported\n")
log.flush()

log.write("ALL OK\n")
log.flush()
log.close()

print("OK - check test_run.log")