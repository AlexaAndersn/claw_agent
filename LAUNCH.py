#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

# Абсолютный путь к Python
PYTHON = r"C:\Users\Диана\AppData\Local\Programs\Python\Python312\python.exe"

# Путь к проекту
PROJECT_DIR = r"D:\claw-агент"

def main():
    os.chdir(PROJECT_DIR)
    print(f"Working directory: {os.getcwd()}")
    print(f"Python: {PYTHON}")
    print(f"Exists: {os.path.exists(PYTHON)}")
    print()
    print("Starting bot...")
    print("=" * 50)
    
    # Запускаем main.py
    os.execv(PYTHON, [PYTHON, os.path.join(PROJECT_DIR, "main.py")])

if __name__ == "__main__":
    main()