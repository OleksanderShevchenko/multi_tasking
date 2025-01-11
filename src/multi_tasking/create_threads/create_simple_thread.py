import threading
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
    # do sequentially
    for i in range(5):
        io_bound_task(i)

    for i in range(5):
        cpu_bound_task(i)
    print("\n *** Run the same in threads ***")
    # run in threads
    for i in range(5):
        t = threading.Thread(target=io_bound_task, args=(i,))
        t.start()

    for i in range(5):
        t = threading.Thread(target=cpu_bound_task, args=(i,))
        t.start()