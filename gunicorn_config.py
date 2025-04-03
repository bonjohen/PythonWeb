"""Gunicorn configuration file for production deployment."""
import multiprocessing
import os

# Bind to 0.0.0.0:8000 by default, but allow environment variables to override
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')

# Number of worker processes
# A common formula is: (2 x number of CPUs) + 1
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Worker class - use gevent for async support
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'gevent')

# Maximum number of simultaneous clients
worker_connections = int(os.getenv('GUNICORN_WORKER_CONNECTIONS', 1000))

# Maximum number of requests a worker will process before restarting
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 50))

# Timeout for worker processes (seconds)
timeout = int(os.getenv('GUNICORN_TIMEOUT', 30))

# Keep the process alive for this many seconds after a SIGTERM
graceful_timeout = int(os.getenv('GUNICORN_GRACEFUL_TIMEOUT', 30))

# Log level
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')

# Access log format
accesslog = os.getenv('GUNICORN_ACCESS_LOG', '-')  # '-' means stdout
errorlog = os.getenv('GUNICORN_ERROR_LOG', '-')    # '-' means stderr

# Process name
proc_name = os.getenv('GUNICORN_PROC_NAME', 'pythonweb')

# Preload the application
preload_app = os.getenv('GUNICORN_PRELOAD_APP', 'True').lower() in ('true', '1', 't')

# Server hooks
def on_starting(server):
    """Log when the server is starting."""
    print("Starting Gunicorn server...")

def on_exit(server):
    """Log when the server is exiting."""
    print("Shutting down Gunicorn server...")

def post_fork(server, worker):
    """Actions to take after forking a worker."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_fork(server, worker):
    """Actions to take before forking a worker."""
    pass

def pre_exec(server):
    """Actions to take before exec-ing a new binary."""
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    """Actions to take when the server is ready to accept connections."""
    server.log.info("Server is ready. Spawning workers...")

def worker_int(worker):
    """Actions to take when a worker receives SIGINT."""
    worker.log.info("worker received INT or QUIT signal")

def worker_abort(worker):
    """Actions to take when a worker receives SIGABRT."""
    worker.log.info(f"worker {worker.pid} aborted")

def worker_exit(server, worker):
    """Actions to take when a worker exits."""
    server.log.info(f"Worker exited (pid: {worker.pid})")
