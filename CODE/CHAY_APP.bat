@echo off
title Password Manager - ATTT Nhom 7
cd /d "%~dp0"
echo.
echo [*] Dang khoi dong Password Manager...
echo.
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] App bi loi! Thong bao loi o tren.
    echo.
    pause
)
