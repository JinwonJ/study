import threading
from collections import Callable

from typing import Dict, List

lock = threading.Lock()


def thread_start(callback: Callable, daemon=True):
    threading.Thread(target=callback, daemon=daemon).start()


def thread_safe_append(target_list: List, item):
    lock.acquire()
    target_list.append(item)
    lock.release()


def thread_safe_set(target_dict: Dict, key, value):
    lock.acquire()
    target_dict.__setitem__(key, value)
    lock.release()
