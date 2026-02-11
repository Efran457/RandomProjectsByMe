@echo off

echo ========================================
echo    Starting Flask Website
echo ========================================
echo.

echo.
echo ========================================
echo Starting the Flask server...
echo Your website will be available at:
echo http://127.0.0.1:5000
echo.
echo Opening browser in 3 seconds...
echo Press Ctrl+C to stop the server
echo ========================================
echo.

start /B timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000

python app.py

pause