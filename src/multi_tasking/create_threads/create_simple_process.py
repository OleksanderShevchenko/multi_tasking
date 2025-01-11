import multiprocessing
from multiprocessing import Process
import time


def io_bound_task(number: int) -> None:
    print(f"\nStart io_bound task #{number}")
    time.sleep(1)
    print(f"\nFinish io_bound task #{number}")


def cpu_bound_task(number: int) -> None:
    print(f"\nStart cpu_bound task #{number}")
    int_val = 1
    for _ in range(20_000_000):
        int_val += 1
    print(f"\nFinish cpu_bound task #{number}")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    # do sequentially
    for i in range(5):
        io_bound_task(i)

    for i in range(5):
        cpu_bound_task(i)
    print("\n *** Run the same in processes ***")
    # run in processes
    for i in range(5):
        p = Process(target=io_bound_task, args=(i,))
        p.start()

    for i in range(5):
        p = Process(target=cpu_bound_task, args=(i,))
        p.start()
