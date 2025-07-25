from typing import Dict
from threading import Lock

# In-memory storage
storage: Dict[str, str | None] = {}
lock = Lock()


def save_transaction(transaction_id: str):
    with lock:
        storage[transaction_id] = None


def save_response(transaction_id: str, response: str):
    with lock:
        storage[transaction_id] = response


def get_response(transaction_id: str) -> str | None:
    with lock:
        return storage.get(transaction_id)


def delete_response(transaction_id: str):
    with lock:
        if transaction_id in storage:
            del storage[transaction_id]
