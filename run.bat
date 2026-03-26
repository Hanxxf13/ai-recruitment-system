@echo off
echo ===========================================
echo AI Recruitment Platform Launch Script
echo ===========================================

REM Setup virtual environments
echo Creating Python Virtual Environment (if not exists)...
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

echo Installing Backend Dependencies...
cd backend
pip install -r requirements.txt

echo Installing Frontend Dependencies...
cd ..\frontend
pip install -r requirements.txt
cd ..

REM Start services
echo Starting FastAPI Backend...
start cmd /k "call venv\Scripts\activate.bat && cd backend && uvicorn main:app --reload --port 8000"

echo Waiting for API to launch...
timeout /t 5 /nobreak > nul

echo Starting Streamlit Frontend...
start cmd /k "call venv\Scripts\activate.bat && cd frontend && streamlit run app.py --server.port 8501"

echo ===========================================
echo Services are Launching!
echo Backend API Docs: http://localhost:8000/docs
echo Frontend App: http://localhost:8501
echo ===========================================
