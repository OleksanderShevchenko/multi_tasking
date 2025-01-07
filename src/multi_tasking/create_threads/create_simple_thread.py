import threading
import time


def io_bound_task(number: int) -> None:
    print(f"\nStart io_bound task #{number}")
    time.sleep(1)
    print(f"\nFinish io_bound task #{number}")


def cpu_bound_task(number: int) -> None:
    print(f"\nStart cpu_bound task #{number}")
    int_val = 1
    for _ in range(1_000_000_000):
        int_val += 1
    print(f"\nFinish cpu_bound task #{number}")


if __name__ == "__main__":
    # do sequentially
    start_time = time.perf_counter()
    for i in range(5):
        io_bound_task(i)
    end_time = time.perf_counter()
    print(f"Sequential io_bound done in {end_time - start_time} seconds.")

    start_time = time.perf_counter()
    for i in range(5):
        cpu_bound_task(i)
    end_time = time.perf_counter()
    print(f"Sequential cpu_bound done in {end_time - start_time} seconds.")

    # do threaded
    start_time = time.perf_counter()
    for i in range(5):
        t = threading.Thread(target=io_bound_task, args=(i,))
        t.start()
    end_time = time.perf_counter()
    print(f"Threaded io_bound done in {end_time - start_time} seconds.")

    start_time = time.perf_counter()
    for i in range(5):
        t = threading.Thread(target=cpu_bound_task, args=(i,))
        t.start()
    end_time = time.perf_counter()
    print(f"Threaded cpu_bound done in {end_time - start_time} seconds.")