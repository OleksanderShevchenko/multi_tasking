import time
from threading import Thread


class DonatorSpender():

    money = 100

    def spend(self) -> None:
        for i in range(1_000_000_000):  # lot of loops to gt into raise condition
            self.money -= 10
        print('Spend done!')

    def donate(self) -> None:
        for i in range(1_000_000_000):
            self.money += 10
        print('Donate done!')


if __name__ == "__main__":
    ds = DonatorSpender()
    t1 = Thread(target=ds.donate, args=())
    t2 = Thread(target=ds.spend, args=())
    t1.start()
    t2.start()
    while t1.is_alive() and t2.is_alive():
        time.sleep(1)

    print(f"Finally we've got {ds.money}")