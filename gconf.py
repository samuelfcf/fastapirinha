import os

bind = os.getenv("BIND")
workers = 1
keepalive = 120
worker_class = "uvicorn.workers.UvicornWorker"
max_request_jitter = 0