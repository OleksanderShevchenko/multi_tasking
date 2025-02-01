import time
from threading import Thread, Condition


class DonatorSpender():
    def __init__(self):
        self.money = 0
        self.condition_variable = Condition()

    def spend(self) -> None:
        for i in range(50_000):
            time.sleep(0.00001)
            self.condition_variable.acquire()
            while self.money < 20:
                self.condition_variable.wait()
            self.money -= 20
            if self.money < 0:  # this condition should never be true
                print(f"Account becomes negative {self.money}")
            self.condition_variable.release()
        print('Spend done!')

    def donate(self) -> None:
        for i in range(100_000):
            time.sleep(0.00001)
            self.condition_variable.acquire()
            self.money += 10
            if self.money < 0:
                print(f"Account still negative {self.money}")
            self.condition_variable.notify()
            self.condition_variable.release()
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