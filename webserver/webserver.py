
import sys
sys.dont_write_bytecode = True

import os
import atexit
import subprocess
from webserver_http import run_server

PID_FILE = "webserver.pid"

def cleanup():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

atexit.register(cleanup)

def main():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = f.read().strip()
            if pid:
                try:
                    # Use taskkill to terminate the process on Windows
                    subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
                    print(f"Terminated existing server with PID: {pid}")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Handle cases where the process doesn't exist or taskkill is not found
                    pass

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    run_server()

if __name__ == "__main__":
    main()
