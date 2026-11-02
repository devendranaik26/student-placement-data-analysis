import subprocess
import sys
import time
import webbrowser

backend = subprocess.Popen([
    sys.executable, "-m", "flask",
    "--app", "flask_app.app",
    "run", "--debug"
])

frontend = subprocess.Popen([
    sys.executable, "-m", "http.server",
    "8000",
    "--directory", "frontend"
])

time.sleep(3)

webbrowser.open("http://127.0.0.1:8000/html/students.html")

print("Student Placement Data Analysis System is running!")
print("Press Ctrl+C to stop both servers.")

try:
    backend.wait()
except KeyboardInterrupt:
    backend.terminate()
    frontend.terminate()
    print("Servers stopped.")