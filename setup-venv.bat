@echo off
echo =========================================
echo   NexusGuard AI - Predictive Maintenance
echo =========================================
echo.

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated.
echo.

echo [2/4] Installing Python dependencies...
cd predictive-maintenance\backend
pip install -r requirements.txt
if errorlevel 1 (
    echo Warning: Some packages failed to install. Trying with flexible versions...
    pip install fastapi uvicorn scikit-learn pandas numpy joblib python-multipart websockets aiofiles
)
echo.

echo [3/4] Starting FastAPI backend...
echo Backend will start on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
start "NexusGuard Backend" cmd /k "call ..\..\venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul
echo.

echo [4/4] Opening dashboard...
cd ..\frontend
start "" "index.html"
cd ..\..
echo.

echo =========================================
echo System is ready!
echo =========================================
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs  
echo - Dashboard: frontend/index.html
echo - WebSocket: ws://localhost:8000/ws/telemetry
echo.
echo Press any key to continue...
pause >nul