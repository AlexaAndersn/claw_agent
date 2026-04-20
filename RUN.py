#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, logging

os.chdir("D:/claw-агент")
sys.path.insert(0, "D:/claw-агент")

logging.basicConfig(
    filename="D:/claw-агент/run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Starting...")

try:
    import main
    import asyncio
    asyncio.run(main.main())
except Exception as e:
    logger.error(f"Error: {e}")
    import traceback
    traceback.print_exc(file=open("D:/claw-агент/err.log", "w"))
finally:
    logger.info("Stopped")