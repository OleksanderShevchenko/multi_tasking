import multiprocessing
import random
import time
from multiprocessing import Process, Array, Barrier
from typing import List

from src.multi_tasking.barrier.matrix_multiplication import MatrixMultiply, MatrixMultipyMultithread


class MatrixMultipyMultiProcess:

    def __init__(self,  matrix_size: int = 3) -> None:
        self._matrix_size: int = matrix_size
        self._core_number = 20
        self._matrix_a: Array = Array('i', [0] * matrix_size * matrix_size, lock=False)
        self._matrix_b: Array = Array('i', [0] * matrix_size * matrix_size, lock=False)
        self._result: Array = Array('i', [0] * matrix_size * matrix_size, lock=False)
        self._init_matrix(self._matrix_a)
        self._init_matrix(self._matrix_b)
        self.__barrier: Barrier = Barrier(self._core_number + 1)

    def _init_matrix(self, matrix: Array) -> None:
        for row in range(self._matrix_size):
            for col in range(self._matrix_size):
                matrix[row * self._matrix_size + col] = random.randint(-9, 9)

    def multiply(self, matrix_a: Array = None, matrix_b: Array = None) -> Array:
        if matrix_a is None:
            matrix_a = self._matrix_a
        if matrix_b is None:
            matrix_b = self._matrix_b
        start = time.time()
        for p in range(self._core_number):
            Process(target=self._calculate_row, args=(p, matrix_a, matrix_b, self._result, self.__barrier,
                                                      self._core_number, self._matrix_size)).start()

        self.__barrier.wait()
        end = time.time()
        print(f"Done in {end - start} sec")

        # for row in range(self.__matrix_size):
        #     print(matrix_a[row], matrix_b[row], self.__result[row])
        # print()
        return self._result

    @staticmethod
    def _calculate_row(proc_id: int,
                       matrix_a: Array,
                       matrix_b: Array,
                       result:Array,
                       barrier: Barrier,
                       proc_count: int,
                       _matrix_size: int) -> None:
        for row in range(proc_id, _matrix_size, proc_count):
            for col in range(_matrix_size):
                for i in range(_matrix_size):
                    result[row * _matrix_size + col] += matrix_a[row * _matrix_size + i] * matrix_b[i * _matrix_size + col]
        barrier.wait()


if __name__ == "__main__":
    matrix_size = 1_000
    matrix_a: list = [[0] * matrix_size for _ in range(matrix_size)]
    matrix_b: list = [[0] * matrix_size for _ in range(matrix_size)]

    mm1 = MatrixMultiply(matrix_size)
    mm1._init_matrix(matrix_a)
    mm1._init_matrix(matrix_b)
    arr1: List[List[int]] =mm1.multiply(matrix_a, matrix_b)

    mm2 = MatrixMultipyMultithread(matrix_size)
    arr2: List[List[int]] =mm2.multiply(matrix_a, matrix_b)

    multiprocessing.set_start_method("spawn")
    mm3 = MatrixMultipyMultiProcess(matrix_size)
    matrix_a_arr: Array = Array('i', [0] * matrix_size * matrix_size, lock=False)
    matrix_b_arr: Array = Array('i', [0] * matrix_size * matrix_size, lock=False)
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix_a_arr[row * matrix_size + col] = matrix_a[row][col]
            matrix_b_arr[row * matrix_size + col] = matrix_b[row][col]
    arr_3: Array = mm3.multiply(matrix_a_arr, matrix_b_arr)

    for row in range(matrix_size):
        for col in range(matrix_size):
            assert arr1[row][col] == arr2[row][col]
    print("Assertion between arr1 and arr2 passed successfully!")

    for row in range(matrix_size):
        for col in range(matrix_size):
            assert arr1[row][col] == arr_3[row * matrix_size + col]
    print("Assertion between arr1 and arr3 passed successfully!")