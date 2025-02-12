import time
from abc import ABC
from multiprocessing import Process, Queue


class Producer(ABC):

    def __init__(self, max_message: int = 30) -> None:
        super().__init__()
        self.__max_message: int = max_message

    def produce(self, queue: Queue) -> None:
        p = Process(target=self._send_message, args=(queue,))
        p.start()

    def _send_message(self, queue_: Queue) -> None:
        iteration: int = 1
        while True:
            queue_.put(f"Message # {iteration}: Hi there!")
            print(f"\nMessage #{iteration} sent!")
            iteration += 1
            if iteration > self.__max_message:
                break
        print("\n ----- Producer done! ----- \n")


class Consumer(ABC):

    def __init__(self) -> None:
        super().__init__()

    def consume(self, queue: Queue) -> None:
        p = Process(target=self._get_message, args=(queue,))
        p.start()

    @staticmethod
    def _get_message(queue_: Queue) -> None:
        while True:
            try:
                message = queue_.get(block=False)
            except Exception as err:
                print(err)
                break
            print(f"\nReceive message: '{message}'!")
            time.sleep(1)
        print("\n ----- Consumer done! ----- \n")


if __name__ == "__main__":
    consumer = Consumer()
    producer = Producer(15)
    q = Queue(maxsize=10)
    producer.produce(q)
    consumer.consume(q)