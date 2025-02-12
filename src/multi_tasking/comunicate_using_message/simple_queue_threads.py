import time
from abc import ABC
from queue import Queue
from threading import Thread


class Producer(ABC):

    def __init__(self, max_message: int = 30) -> None:
        super().__init__()
        self.__max_message: int = max_message

    def produce(self, queue: Queue) -> None:

        def _send_message(queue_: Queue) -> None:
            iteration: int = 1
            while True:
                queue_.put(f"Message # {iteration}: Hi there!")
                print(f"\nMessage #{iteration} sent!")
                iteration += 1
                if iteration > self.__max_message:
                    break
            print(" ----- Producer done! ----- ")

        th = Thread(target=_send_message, args=(queue,))
        th.start()


class Consumer(ABC):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def consume(queue: Queue) -> None:

        def _get_message(queue_: Queue) -> None:
            while True:
                try:
                    message = queue_.get(block=False)
                except Exception as err:
                    print(err)
                    break
                print(f"\nReceive message: '{message}'!")
                time.sleep(1)
            print(" ----- Consumer done! ----- ")

        Thread(target=_get_message, args=(queue,)).start()


if __name__ == "__main__":
    consumer = Consumer()
    producer = Producer(15)
    q = Queue(maxsize=10)
    producer.produce(q)
    consumer.consume(q)