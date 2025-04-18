import threading
import time
from functools import wraps
from typing import Literal, get_args, Callable, ParamSpec, TypeVar, Concatenate
from typeguard import typechecked

from klocker.exception import LockerLocked
from klocker.interface import LockerInterface
from klocker.localstate import ThreadLocalState

ON_BLOCKED_T = Literal['wait', 'leave', 'raise']
ON_BLOCKED: tuple[ON_BLOCKED_T, ...] = get_args(ON_BLOCKED_T)

P = ParamSpec("P")
R = TypeVar("R")


class SimpleLocker(LockerInterface):
    """
    A simple locker class to manage shared resources.
    """
    __slots__ = ('_lock', '_state', '_on_locked')

    @typechecked
    def __init__(self, *, on_blocked: ON_BLOCKED_T = 'wait'):
        """
        Initializes the locker with a blocking behavior.
        """
        self._lock = threading.Lock()
        self._on_locked = on_blocked
        self._state = ThreadLocalState()

    def __enter__(self):
        """
        Acquires the lock based on the blocking behavior.
        """
        self._state.acquired = False
        if not self._lock.acquire(blocking=False):
            if self._on_locked == 'wait':
                self._lock.acquire()
            elif self._on_locked == 'leave':
                return self
            elif self._on_locked == 'raise':
                raise LockerLocked()

        self._state.acquired = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the lock if it was acquired.
        """
        if self.acquired:
            self._lock.release()

    @property
    def acquired(self):
        """
        Checks if the lock is currently acquired.
        """
        return self._state.acquired

    def execute_with_locker(self, func: Callable[Concatenate[bool, P], R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Executes a function with the lock, passing the lock status.
        """
        with self:
            acquired = self.acquired
            return func(acquired, *args, **kwargs)

    def execute_if_acquired(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Executes a function only if the lock is acquired.
        """
        with self:
            if self.acquired:
                return func(*args, **kwargs)

    def with_locker(self, func: Callable[Concatenate[bool, P], R]) -> Callable[P, R]:
        """
        Decorator to execute a function with the lock.
        """
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return self.execute_with_locker(func, *args, **kwargs)

        return wrapper

    def if_acquired(self, func: Callable[P, R]) -> Callable[P, R]:
        """
        Decorator to execute a function only if the lock is acquired.
        """
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
            self.execute_if_acquired(func, *args, **kwargs)

        return wrapper


def start_threads(worker_func: Callable, _last_idx: int = 0, _n_threads: int = 10) -> int:
    """
    Starts multiple threads to execute a worker function.
    """
    threads = [
        threading.Thread(target=worker_func, name=f"Thread-{idx}") for idx in
        range(_last_idx, _last_idx + _n_threads)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return _last_idx + _n_threads


def test():
    """
    Test function to demonstrate the usage of SimpleLocker.
    """
    locker = SimpleLocker(on_blocked='leave')
    last_idx = 0
    n_threads = 10

    def execute_with_locker(acquired: bool):
        """
        Prints lock status and simulates work inside the lock.
        """
        if acquired:
            print(f"[{threading.current_thread().name}] Acquired the lock.")
            time.sleep(0.05)  # Simula trabajo dentro del bloqueo
        else:
            print(f"[{threading.current_thread().name}] Could not acquire the lock.")

    def execute_if_acquired():
        """
        Prints a message if the lock is acquired.
        """
        print(f"[{threading.current_thread().name}] Acquired the lock.")
        time.sleep(0.05)  # Simula trabajo dentro del bloqueo

    @locker.with_locker
    def with_locker(acquired: bool):
        """
        Decorated function to execute with the lock.
        """
        if acquired:
            print(f"[{threading.current_thread().name}] Acquired the lock.")
            time.sleep(0.05)
        else:
            print(f"[{threading.current_thread().name}] Could not acquire the lock.")

    @locker.if_acquired
    def if_acquired():
        """
        Decorated function to execute only if the lock is acquired.
        """
        print(f"[{threading.current_thread().name}] Acquired the lock.")
        time.sleep(0.05)

    def execute_with_locker_manual(_locker: LockerInterface):
        """
        Manually acquires the lock and executes work inside it.
        """
        with _locker:
            if _locker.acquired:
                print(f"[{threading.current_thread().name}] Acquired the lock.")
                time.sleep(0.05)  # Simulates work inside the lock
            else:
                print(f"[{threading.current_thread().name}] Could not acquire the lock.")

    def execute_if_acquired_manual(_locker: LockerInterface):
        """
        Manually checks if the lock is acquired before executing work.
        """
        with _locker:
            if not _locker.acquired:
                return

            print(f"[{threading.current_thread().name}] Acquired the lock.")
            time.sleep(0.05)  # Simulates work inside the lock

    # Uncomment one of the following to test different scenarios:
    # start_threads(lambda: locker.execute_with_locker(execute_with_locker), last_idx, n_threads)
    # start_threads(lambda: locker.execute_if_acquired(execute_if_acquired), last_idx, n_threads)
    # start_threads(with_locker, last_idx, n_threads)
    # start_threads(if_acquired, last_idx, n_threads)
    # start_threads(lambda: execute_with_locker_manual(locker), last_idx, n_threads)
    start_threads(lambda: execute_if_acquired_manual(locker), last_idx, n_threads)


if __name__ == "__main__":
    test()

