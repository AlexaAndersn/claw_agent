@echo off
chcp 65001 >nul
title Claw-Agent

cd /d D:\claw-агент

echo ========================================
echo    Claw-Agent - BOT LAUNCHER v2
echo ========================================
echo.

set PYTHON="C:\Users\Диана\AppData\Local\Programs\Python\Python312\python.exe"

echo Using Python: %PYTHON%
echo.

echo [1] Testing Python...
%PYTHON% --version
echo.

echo [2] Import test...
%PYTHON% -c "print('Python works!')"
echo.

echo [3] Starting bot...
echo.

%PYTHON% main.py

echo.
echo ========================================
echo    BOT STOPPED
echo ========================================
pause