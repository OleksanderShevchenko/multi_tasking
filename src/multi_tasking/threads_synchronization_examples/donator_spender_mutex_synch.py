import time
from threading import Thread, Lock


class DonatorSpender():
    def __init__(self):
        self.money = 100
        self.mutex = Lock()

    def spend(self) -> None:
        for i in range(100_000):  # lot of loops to gt into raise condition
            time.sleep(0.00001)
            self.mutex.acquire()
            self.money -= 10
            self.mutex.release()
        print('Spend done!')

    def donate(self) -> None:
        for i in range(100_000):
            time.sleep(0.00001)
            self.mutex.acquire()
            self.money += 10
            self.mutex.release()
        print('Donate done!')


if __name__ == "__main__":
    ds = DonatorSpender()
    t1 = Thread(target=ds.donate, args=())
    t2 = Thread(target=ds.spend, args=())
    start = time.perf_counter()
    t1.start()
    t2.start()
    while t1.is_alive() and t2.is_alive():
        time.sleep(1)
    end = time.perf_counter()
    print(f"Finally we've got {ds.money}! It takes {end-start} sec.")