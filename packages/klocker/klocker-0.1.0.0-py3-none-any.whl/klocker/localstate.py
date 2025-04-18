import threading
from typeguard import typechecked


class ThreadLocalState:
    """Clase para manejar el estado específico de cada hilo."""
    __slots__ = ('_thread_local',)

    def __init__(self):
        self._thread_local = threading.local()

    @property
    def acquired(self) -> bool:
        """Obtiene el estado de 'acquired' para el hilo actual."""
        return getattr(self._thread_local, 'acquired', False)

    @acquired.setter
    @typechecked
    def acquired(self, value: bool):
        """Establece el estado de 'acquired' para el hilo actual."""
        self._thread_local.acquired = value

    def reset(self):
        """Resetea el estado de 'acquired' para el hilo actual."""
        self._thread_local.acquired = False
