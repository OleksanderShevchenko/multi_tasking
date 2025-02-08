import time
from multiprocessing import Process, Array
from numpy.typing import  ArrayLike


def print_array(array: ArrayLike)-> None:
    while True:
        print(*array, sep=", ")
        time.sleep(1)


if __name__ == "__main__":
    array = [-1] * 10
    # array pass as a copy
    proc = Process(target=print_array, args=(array,))
    proc.start()
    print("Process 1 start")
    for _ in range(10):
        time.sleep(2)
        for i in range(10):
            array[i] += 1
    proc.kill()
    print("Process 1 done!")


    array = Array('i', [-1] * 10)
    # now array is shared between processes
    proc = Process(target=print_array, args=(array,))
    proc.start()
    print("Process 2 start")
    for _ in range(20):
        time.sleep(2)
        for i in range(10):
            array[i] += 1
    proc.kill()
    print("Process 2 done!")
