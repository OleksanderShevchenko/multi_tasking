from threading import Condition


class WaitGroup:

    def __init__(self) -> None:
        self._cv: Condition = Condition()
        self._wait_count: int = 0

    def add(self, count: int) -> None:
        with self._cv:
            self._wait_count += count

    def done(self) -> None:
        with self._cv:
            if self._wait_count > 0:
                self._wait_count -= 1
            if self._wait_count == 0:
                self._cv.notify_all()

    def wait(self) -> None:
        with self._cv:
            while self._wait_count > 0:
                self._cv.wait()