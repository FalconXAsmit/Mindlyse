import subprocess
import sys
import time
import threading

def run_backend():
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", "--reload", "--port", "8000"
    ])

def run_frontend():
    time.sleep(2)
    subprocess.run([
        sys.executable, "-m", "streamlit", 
        "run", "app.py", "--server.port", "8501"
    ])

if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)
    
    backend_thread.start()
    frontend_thread.start()
    
    backend_thread.join()
    frontend_thread.join()