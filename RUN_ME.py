# -*- coding: utf-8 -*-
import os, sys, subprocess

print("=== Starting Claw-Agent ===")

os.chdir(r"D:\claw-агент")
print(f"Working dir: {os.getcwd()}")

result = subprocess.run(
    ["py", "main.py"],
    capture_output=True,
    text=True,
    timeout=30
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

input("\nPress Enter to exit...")