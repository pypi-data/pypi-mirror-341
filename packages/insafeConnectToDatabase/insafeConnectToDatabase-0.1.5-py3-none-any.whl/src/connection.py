from letta_client import Letta

def connect():
    client = Letta(base_url="http://localhost:8283")
    return client;

__all__ = ["connect"]
