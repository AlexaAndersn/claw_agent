@echo off
chcp 65001>nul
cd /d D:\claw-агент
echo Starting Claw-Agent...
py main.py
echo.
echo Press any key to exit...
pause >nul