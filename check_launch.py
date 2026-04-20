# -*- coding: utf-8 -*-
import sys, os, subprocess, logging

# Setup logging
logging.basicConfig(
    filename="D:/claw-агент/bot_run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)
log.info("=== Starting launch script ===")

try:
    os.chdir("D:/claw-агент")
    log.info(f"Changed dir to: {os.getcwd()}")
    
    # Check if main.py exists
    if os.path.exists("main.py"):
        log.info("main.py exists")
        
        # Try to run
        result = subprocess.run(
            ["py", "main.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        log.info(f"Return code: {result.returncode}")
        log.info(f"STDOUT: {result.stdout[:500]}")
        log.info(f"STDERR: {result.stderr[:500]}")
    else:
        log.error("main.py NOT FOUND")
        
except Exception as e:
    log.error(f"Error: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")