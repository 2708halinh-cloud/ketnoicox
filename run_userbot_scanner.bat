@echo off
chcp 65001 >nul
setlocal

cd /d %~dp0

echo [INFO] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
  echo [ERROR] Dependency installation failed.
  pause
  exit /b 1
)

if not exist ".env" (
  echo [WARN] .env not found. Creating from .env.example ...
  copy /Y ".env.example" ".env" >nul
  echo [WARN] Please update .env values (API_ID, API_HASH, ADMIN_ID) before next run.
)

echo [INFO] Starting userbot_scanner.py ...
python userbot_scanner.py

echo.
echo [INFO] Process ended.
pause
