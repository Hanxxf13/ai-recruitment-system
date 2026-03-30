import subprocess
import sys
import os
import signal
import time
from threading import Thread

def log_stream(stream, prefix):
    """Logs a stream with a colored prefix."""
    for line in iter(stream.readline, b''):
        # Add color and prefix
        print(f"{prefix} | {line.decode().strip()}", flush=True)

def run():
    # Detect the correct python executable inside .venv
    if os.name == 'nt':
        python_exe = os.path.join(".venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join(".venv", "bin", "python")

    if not os.path.exists(python_exe):
        python_exe = sys.executable

    print("\n" + "="*50)
    print(" NUKHBA ELITE Unified Process Manager")
    print("="*50 + "\n")

    # Command 1: FastAPI Backend
    # Use -m uvicorn to ensure correct module resolution
    backend_cmd = [
        python_exe, "-m", "uvicorn", "backend.main:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ]

    # Command 2: Streamlit Frontend
    frontend_cmd = [
        python_exe, "-m", "streamlit", "run", "frontend/app.py",
        "--server.port", "8501", "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ]

    print(f"[PROCESS] Starting Backend on port 8000...")
    backend_proc = subprocess.Popen(
        backend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1
    )

    print(f"[PROCESS] Starting Frontend on port 8501...")
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1
    )

    # Start logging threads
    t1 = Thread(target=log_stream, args=(backend_proc.stdout, "\033[94m[BACKEND]\033[0m"))
    t2 = Thread(target=log_stream, args=(backend_proc.stderr, "\033[94m[BACKEND]\033[0m"))
    t3 = Thread(target=log_stream, args=(frontend_proc.stdout, "\033[93m[FRONTEND]\033[0m"))
    t4 = Thread(target=log_stream, args=(frontend_proc.stderr, "\033[93m[FRONTEND]\033[0m"))

    for t in [t1, t2, t3, t4]:
        t.daemon = True
        t.start()

    print("\n" + "="*50)
    print(" SERVICES RUNNING!")
    print(f" Web App:    http://localhost:8501")
    print(f" API:        http://localhost:8000")
    print(f" API Docs:   http://localhost:8000/docs")
    print("="*50 + "\n")
    print("Press Ctrl+C to stop all services...\n")

    try:
        while True:
            # Check if any process has died
            if backend_proc.poll() is not None:
                print("\n[ERROR] Backend process terminated unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("\n[ERROR] Frontend process terminated unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        # Kill processes
        if os.name == 'nt':
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(backend_proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(frontend_proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            backend_proc.terminate()
            frontend_proc.terminate()
        print("All services stopped.")

if __name__ == "__main__":
    run()
