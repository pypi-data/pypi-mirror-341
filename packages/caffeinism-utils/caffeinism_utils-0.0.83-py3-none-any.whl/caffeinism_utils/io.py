import threading
from abc import ABC, abstractmethod
from collections import deque


class BaseQueueIO(ABC):
    _exc: Exception

    def __init__(self):
        self._data_available = threading.Condition(threading.Lock())
        self._eof = False
        self._exc = None
        self.closed = False

    @abstractmethod
    def _write(self, data: bytes) -> None:
        """write data"""

    def write(self, data: bytes) -> None:
        with self._data_available:
            self._write(data)
            self._data_available.notify_all()

    @abstractmethod
    def _read(self, size: int = -1) -> bytes | None:
        """read data"""

    def read(self, size: int = -1) -> bytes:
        with self._data_available:
            while True:
                if self._exc is not None:
                    raise self._exc

                data = self._read(size)

                if data is None:
                    if self._eof:
                        return b""
                    self._data_available.wait()
                else:
                    return data

    def close(self):
        with self._data_available:
            self._eof = True
            self._data_available.notify_all()

    def seekable(self):
        return False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def exc(self, exc):
        with self._data_available:
            self._exc = exc
            self._data_available.notify_all()


class PopIO(BaseQueueIO):
    def __init__(self):
        super().__init__()
        self._buffer = deque()

    def _write(self, data: bytes) -> None:
        self._buffer.append(data)

    def pop(self):
        while self._buffer:
            yield self._buffer.popleft()

    def _read(self, size: int = -1) -> bytes | None:
        ret = []
        length = 0

        while self._buffer and (size < 0 or length < size):
            item = self._buffer.popleft()
            length += len(item)
            ret.append(item)

        if not ret:
            return None

        if length <= size or size < 0:
            return b"".join(ret)

        mem = memoryview(ret[-1])
        last, remain = mem[: size - length], mem[size - length :]
        self._buffer.appendleft(remain)
        ret[-1] = last
        return b"".join(ret)

    def tell(self):
        pass


class QueueIO(BaseQueueIO):
    def __init__(self):
        super().__init__()
        self._buffer = bytearray()

    def _write(self, data: bytes) -> None:
        self._buffer.extend(data)

    def _read(self, size: int = -1) -> bytes | None:
        if size < 0:
            size = len(self._buffer)

        ret = bytes(memoryview(self._buffer)[:size])

        if not ret:
            return None

        del self._buffer[:size]
        return ret
