import os, sys, subprocess, threading, time

def run_bot():
    os.chdir("D:/claw-агент")
    subprocess.Popen([sys.executable, "main.py"])

thread = threading.Thread(target=run_bot)
thread.start()
print("Bot started in background!")
thread.join(timeout=1)