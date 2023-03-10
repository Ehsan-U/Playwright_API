# High-Performance, High-Concurrency FastAPI Endpoint for Playwright-Python

This repository contains a high-performance, high-concurrency FastAPI endpoint for web scraping using Playwright and Python. The endpoint provides a Python API for interacting with Playwright and allows developers to automate web browsers in a scalable, efficient manner.

## Features
- Built with FastAPI, a modern, fast, web framework for building APIs with Python
- Optimized for high performance and high concurrency using asynchronous programming
- Easy to extend and customize to meet specific requirements
- Redis cache supported
- Ready to deploy in cloud

## Prerequisites
- Python 3.7 or higher
- Playwright-Python library
- FastAPI and its dependencies
- Redis

## Getting Started
1. Clone the repository:
2. Navigate to the project directory:
3. ``` pip install -r requirements.txt ```
4. Setup redis
```
" Use WSL ubuntu on windows "
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
sudo service redis-server restart
```
5. ``` uvicorn main:app ``` this will start the endpoint
6. Now you can use that endpoint via http://127.0.0.1:8000

## Usage 
```python
import requests

# Make a POST request to the endpoint with the Request payload
url = "http://localhost:8000/"
payload = {
    "url": "https://www.example.com",
}

# Send the request
response = requests.post(url, json=payload)

# Access the response data
data = response.json()
print(data)

```
## Extra arguments 
```python
import requests

# Make a POST request to the endpoint with the Request payload
url = "http://localhost:8000/"
payload = {
    "url": "https://www.example.com",
    # xpath or css selector
    "wait_until": "selector",
    # selector timeout (milliseconds)
    "timeout": 1000,
    # explicit wait after page loaded (milliseconds)
    "wait_for": 5000,
    # block images loading
    "images_enabled": False
}

# Send the request
response = requests.post(url, json=payload)

# Access the response data
data = response.json()
print(data)

```


## Contributions
Contributions are welcome! If you have an idea for a new feature or find a bug, please open an issue or submit a pull request.



