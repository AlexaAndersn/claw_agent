@echo off
chcp 65001 >nul
title Claw-Agent

cd /d D:\claw-агент

echo ========================================
echo    Claw-Agent - Start
echo ========================================

:start
py main.py
echo.
echo Bot stopped. Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto start