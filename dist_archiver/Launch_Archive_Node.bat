@echo off
echo ========================================================
echo   SOVEREIGN STORAGE ARCHIVER: STARTING REVENUE NODE
echo   Partner: meta2graei@gmail.com
echo ========================================================
echo.
echo 1. Starting Local Sovereign API (Port 8080)...
start /B python Lujan_SaaS_API.py
echo.
echo 2. Your Archive Drop is now active at: http://localhost:8080
echo.
echo 3. To make it PUBLIC on the market, run this in a new terminal:
echo    cloudflared.exe tunnel --url http://localhost:8080
echo.
echo Node Status: ACTIVE
echo Revenue Mode: ENABLED
pause
