#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess

# Путь к Python
PYTHON = r"C:\Users\Диана\AppData\Local\Programs\Python\Python312\python.exe"

# Путь к проекту
PROJECT = r"D:\claw-агент\main.py"

print("Starting Claw-Agent...")
print(f"Python: {PYTHON}")
print(f"Project: {PROJECT}")
print()

# Запуск
subprocess.call([PYTHON, PROJECT])