@echo off
title DYT01 Worker Manager
color 0A
echo ========================================
echo    DYT01 WORKER MANAGER
echo ========================================
echo.

cd /d E:\DYT_01

echo Dang khoi dong workers...
echo.

start "Worker Manager" /MIN python worker_manager.py

timeout /t 2 /nobreak >nul

echo Workers da duoc khoi dong!
echo Kiem tra cua so "Worker Manager" de xem log
echo.

pause