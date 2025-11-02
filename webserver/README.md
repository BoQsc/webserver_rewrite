
# Webserver Project

## Project Overview

This project is a simple Python web server. The project is structured in a modular way, with different functionalities separated into different files.

## Setup

The initial setup of the project involved the following steps:

1.  **File Renaming:** The core files (`webserver`, `webserver_api`, `webserver_config`, `webserver_routing`, `webserver_http`) were renamed to have a `.py` extension.
2.  **Refactoring:** The HTTP server logic was moved from `webserver.py` to `webserver_http.py`. The `webserver.py` file now serves as the main entry point to the application, importing and running the server from `webserver_http.py`.

## Running the Server

To run the web server, execute the following command in your terminal from the `webserver` directory:

```bash
python webserver.py
```

This will start the server on `http://localhost:8000`.

Alternatively, you can run the server in the background using the following PowerShell command:

```powershell
Start-Process -FilePath "python" -ArgumentList "webserver.py" -NoNewWindow
```

## Stopping the Server

If you are running the server in the foreground, you can stop it by pressing `Ctrl+C` in your terminal.

If you are running the server in the background, you can stop it by using the following command in your terminal:

```bash
taskkill /IM python.exe
```

This will terminate all running Python processes.
