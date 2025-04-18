from abc import ABC, abstractmethod
from typing import Literal, get_args, ParamSpec, TypeVar

ON_BLOCKED_T = Literal['wait', 'leave', 'raise']
ON_BLOCKED: tuple[ON_BLOCKED_T, ...] = get_args(ON_BLOCKED_T)

P = ParamSpec("P")
R = TypeVar("R")


class LockerInterface(ABC):
    """Interfaz para un locker."""

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    @property
    @abstractmethod
    def acquired(self) -> bool:
        ...
