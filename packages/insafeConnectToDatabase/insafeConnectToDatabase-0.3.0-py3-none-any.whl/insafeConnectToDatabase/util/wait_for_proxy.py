import time
import socket


def wait_for_proxy(host="127.0.0.1", port=5432, timeout=10):
    """Wait until the proxy binds to the specified host and port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"Cloud SQL Proxy is ready on {host}:{port}")
                return True
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(1)
    raise RuntimeError(f"Could not connect to Cloud SQL Proxy on {host}:{port} in {timeout} seconds")
