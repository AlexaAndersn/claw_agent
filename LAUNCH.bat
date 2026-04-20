@echo off
chcp 65001 >nul
title Claw-Agent

cd /d D:\claw-агент

echo.
echo ========================================
echo    Claw-Agent - BOT LAUNCHER
echo ========================================
echo.

echo Current Directory: %CD%
echo.

echo Checking Python...
python --version
echo.

echo Checking main.py...
if exist "main.py" (
    echo [OK] main.py found
) else (
    echo [ERROR] main.py NOT FOUND!
    pause
    exit
)
echo.

echo ========================================
echo    STARTING BOT NOW...
echo ========================================
echo.

python main.py

echo.
echo ========================================
echo    BOT STOPPED
echo ========================================
echo Press any key to exit...
pause >nul