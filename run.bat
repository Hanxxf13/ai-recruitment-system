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

REM Start Unified Backend and Frontend (Streamlit at 8501, FastAPI at 8000)
echo Starting Nukhba Elite services...
echo.
echo ===========================================
echo  Services initializing...
echo  Web App (Streamlit): http://localhost:8501
echo  API (FastAPI):       http://localhost:8000
echo ===========================================
echo.

REM Open browser to the Streamlit frontend
start http://localhost:8501

REM Run the unified process manager
python run_all.py
