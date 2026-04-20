@echo off
chcp 65001 >nul
echo ========================================
echo    Claw-Agent Launcher
echo ========================================
echo.

echo [1] Finding Python...
py --version 2>&1

if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from python.org
    pause
    exit /b 1
)

echo.
echo [2] Python found, starting bot...
echo ========================================
echo.

py main.py

echo.
echo ========================================
echo [BOT STOPPED]
echo ========================================
pause