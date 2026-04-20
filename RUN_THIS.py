import os
import sys
import subprocess

# Абсолютные пути
PYTHON = r"C:\Users\Диана\AppData\Local\Programs\Python\Python312\python.exe"
PROJECT = r"D:\claw-агент\main.py"

# Создаем процесс
process = subprocess.Popen(
    [PYTHON, PROJECT],
    cwd=PROJECT.replace("\\main.py", ""),
    creationflags=subprocess.CREATE_NEW_CONSOLE
)

print(f"Bot started! PID: {process.pid}")
print("Press Enter to stop...")
input()

process.terminate()
print("Bot stopped.")