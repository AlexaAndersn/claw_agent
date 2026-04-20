@echo off
chcp 65001 >nul
echo Checking Python...

where py

if %errorlevel% neq 0 (
    echo Python not found in PATH!
    echo.
    echo Please install Python or add to PATH
    pause
    exit /b 1
)

echo.
echo Python found! Starting bot...
echo.

py main.py

echo.
echo Bot stopped.
pause