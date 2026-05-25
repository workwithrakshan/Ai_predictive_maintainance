@echo off
echo =========================================
echo   NexusGuard AI - Predictive Maintenance
echo =========================================
echo.

echo [1/3] Installing Python dependencies...
cd predictive-maintenance\backend
pip install fastapi uvicorn scikit-learn pandas numpy joblib python-multipart websockets aiofiles
echo.

echo [2/3] Starting FastAPI backend...
start "NexusGuard Backend" uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo Backend started on http://localhost:8000
echo.

echo [3/3] Opening dashboard...
timeout /t 3 /nobreak >nul
start "" "..\frontend\index.html"
echo.

echo System is ready!
echo - API Docs: http://localhost:8000/docs
echo - Dashboard: Open frontend\index.html in browser
echo - WebSocket: ws://localhost:8000/ws/telemetry
echo.
echo Press any key to stop the backend...
pause >nul
taskkill /f /im "python.exe" /fi "windowtitle eq NexusGuard Backend*" 2>nul