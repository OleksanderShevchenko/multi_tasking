import datetime
import time
from threading import Barrier, Thread

barrier = Barrier(2)

def wait_on_barrier(thread_name: str, time_sleep: int ) -> None:
    for _ in range(3):
        print(f"\n{thread_name} thread is running ...")
        time.sleep(time_sleep)
        print(f"\n{thread_name} thread is waiting on a barrier ...")
        barrier.wait()
    print(f"{thread_name} is finished at {datetime.datetime.now(datetime.UTC)} - {time.time_ns()}!")


if __name__ == "__main__":
    red = Thread(target=wait_on_barrier, args=("red ", 4))
    blue = Thread(target=wait_on_barrier, args=("blue", 10))
    red.start()
    blue.start()