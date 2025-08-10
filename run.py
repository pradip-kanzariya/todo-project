import subprocess
import time
import requests
import webbrowser

# Start FastAPI with autoreload
fastapi_process = subprocess.Popen(
    ["fastapi", "dev", "app.py", "--port", "8000"],
    cwd="fastapi"
)

# Wait until FastAPI is running
for _ in range(20):  # ~10 seconds
    try:
        requests.get("http://127.0.0.1:8000/todo")
        print("✅ FastAPI is running")
        break
    except requests.exceptions.ConnectionError:
        time.sleep(0.5)
else:
    print("❌ FastAPI failed to start")
    fastapi_process.terminate()
    exit(1)

# Start Streamlit
streamlit_process = subprocess.Popen(
    ["streamlit", "run", "main.py"],
    cwd="streamlit"
)

# Open Streamlit in browser
time.sleep(2)
# webbrowser.open("http://localhost:8501")

try:
    fastapi_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    print("\nShutting down...")
    fastapi_process.terminate()
    streamlit_process.terminate()
