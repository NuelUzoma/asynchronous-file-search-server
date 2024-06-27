# Asynchronous File Search Server

## Project Scope

This project implements an asynchronous Python server designed to handle concurrent file search requests efficiently. The server supports multiple search algorithms, allowing performance comparison across various file sizes and query rates.

## Features

- Asynchronous server to handle multiple clients concurrently.
- Support for different file search algorithms:
  - Asynchronous aiofiles search
  - Linear Search (Standard I/O)
  - Jump Search Algorithm
  - Binary Search Algorithm
  - Exponential Search Algorithm
  - Knuth-Morris-Pratt (KMP) Algorithm
  - Multi-threaded search (concurrent.futures)
- SSL/TLS support for secure connections.
- Detailed logging and error handling.
- Performance testing script to benchmark search algorithms.

## Prerequisites

- Python 3.8+
- Virtualenv
- Linux environment

## Setup Instructions

### 1. Clone or Unzip the Repository

```bash
git clone <repository_url>
cd asynchronous-file-search-server
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory with the following content:

```makefile
HOST=127.0.0.1
PORT=8888
REREAD_ON_QUERY=True
```

### 5. Configure SSL (Optional)
If you want to enable SSL, update the config/config.cfg file:

```bash
linuxpath=/path/to/200k.txt
use_ssl=true
certfile=path/to/certfile.pem
keyfile=path/to/keyfile.pem
```

### 6. Configure Systemd Service
Create a systemd service file at /etc/systemd/system/async_server.service with the following content:

```ini
[Unit]
Description=Async Python Server
After=network.target

[Service]
Type=simple
User=<your_username>
WorkingDirectory=/path/to/asynchronous-file-search-server
ExecStart=/path/to/venv/bin/python3 /path/to/asynchronous-file-search-server/async_server.py
Restart=always
RestartSec=15

[Install]
WantedBy=multi-user.target
```

Replace <your_username> with your Linux username and /path/to/async-file-search-server with the full path to the project directory.

### 7. Enable and Start the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable async_server.service
sudo systemctl start async_server.service
```

### 8. Check Service Status
```bash
sudo systemctl status async_server.service
```

## Running Performance Tests

### 1. Configure Performance Test Environment
Update the performance_test.py script with appropriate file paths and queries.

### 2. Run Performance Tests
```bash
python performance_test.py
```

### 3. Analyze Performance Results
Collect and analyze the results generated by the performance tests to compare the execution times of different search algorithms.

## Running Unit Tests

### 1. Install Test Dependencies
```bash
pip install -r requirements-test.txt
```

### 2. Run Tests
```bash
pytest tests/
```

## Logging Configuration
The logging configuration is set up in config/logging_config.py. Adjust the logging settings as needed for your environment.

