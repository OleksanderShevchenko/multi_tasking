import time
from threading import Thread


class SimpleWorker:

    def __init__(self, duration: int = 5) -> None:
        self.__time_to_work = duration  # sec

    def __private_task(self) -> None:
        print('Run private task in separate thread')
        time.sleep(self.__time_to_work)
        print ("Private task done ...")

    def do_work(self) -> None:
        t = Thread(target=self.__private_task, args=())
        t.start()
        print("Main worker is waiting for private task ...")
        t.join()
        print("Main thread is unblocked . Tasks done...")


if __name__ == "__main__":
    sw = SimpleWorker(10)
    sw.do_work()