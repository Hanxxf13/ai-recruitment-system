@echo off
echo ===========================================
echo  NUKHBA ELITE — Recruitment Platform
echo ===========================================

REM Setup virtual environment
if not exist .venv (
    echo Creating Python virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat

REM Install all dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
pip install -r backend/requirements.txt --quiet

REM Start Backend API (serves frontend at http://localhost:8000)
echo Starting Nukhba Elite backend...
start cmd /k "call .venv\Scripts\activate.bat && cd /d %~dp0 && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 4 /nobreak > nul

echo ===========================================
echo  Services Running!
echo.
echo  Web App:    http://localhost:8000/
echo  Login Page: http://localhost:8000/web/index.html
echo  API Docs:   http://localhost:8000/docs
echo ===========================================

REM Open browser
start http://localhost:8000/web/index.html
