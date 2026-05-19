@echo off
echo ========================================================
echo   CYBERDNA: SAFE C-DRIVE ARCHIVER (DESTRUCTIVE MODE)
echo ========================================================
echo.
echo WARNING: This will compress unused files in your personal folders
echo and DELETE the originals to instantly free up space on your C: Drive.
echo.
pause
echo.
python c_drive_archiver.py --execute
