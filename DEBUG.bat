@echo off
chcp 65001 >nul
title Claw-Agent

cd /d D:\claw-агент

echo.
echo ========================================
echo    Claw-Agent - DEBUG LAUNCHER
echo ========================================
echo.

echo [1] Python location:
where python
echo.

echo [2] Python version:
python --version
echo.

echo [3] Python executable:
echo %PYTHON%
echo.

echo [4] Running test import...
python -c "print('Test: OK')"
echo.

echo [5] Running main.py with full output...
echo.

python -u main.py 2>&1

echo.
echo ========================================
echo    BOT STOPPED
echo ========================================
echo Exit code: %errorlevel%
echo.
pause