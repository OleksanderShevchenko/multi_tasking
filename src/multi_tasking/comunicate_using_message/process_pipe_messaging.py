import time
from abc import ABC
from datetime import datetime
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from typing import Tuple


class PingPong(ABC):

    def __init__(self, max_message: int = 30) -> None:
        super().__init__()
        self.__max_message: int = max_message
        ab: Tuple[Connection] = Pipe()
        self._pipe_end_a: Connection = ab[0]
        self._pipe_end_b: Connection = ab[1]

    def pingpong(self) -> None:
        p1 = Process(target=self._ping, args=(self._pipe_end_a,))
        p1.start()
        p2 = Process(target=self._pong, args=(self._pipe_end_b,))
        p2.start()

    def _ping(self, pipe_end: Connection) -> None:
        iteration: int = 1
        while True:
            pipe_end.send(f"Ping #{iteration} {datetime.now().strftime("%H:%M:%S")}")
            pong = pipe_end.recv()
            print(pong)
            time.sleep(1)
            iteration += 1
            if iteration > self.__max_message:
                break
        print("\n ----- Ping done! ----- \n")

    def _pong(self, pipe_end: Connection) -> None:
        iteration: int = 1
        while True:
            ping = pipe_end.recv()
            print(ping)
            time.sleep(1)
            pipe_end.send(f"Pong #{iteration} {datetime.now().strftime("%H:%M:%S")}")
            iteration += 1
            if iteration > self.__max_message:
                break
        print("\n ----- Pong done! ----- \n")


if __name__ == "__main__":
    pp = PingPong()
    pp.pingpong()