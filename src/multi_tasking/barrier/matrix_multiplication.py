import random
import time
from threading import Thread, Barrier


class MatrixMultiply:

    def __init__(self, matrix_size: int = 3) -> None:
        self._matrix_size: int = matrix_size
        self._matrix_a: list = [[0] * matrix_size for _ in range(matrix_size)]
        self._matrix_b: list = [[0] * matrix_size for _ in range(matrix_size)]
        self._result: list = [[0] * matrix_size for _ in range(matrix_size)]
        self._init_matrix(self._matrix_a)
        self._init_matrix(self._matrix_b)


    def _init_matrix(self, matrix: list) -> None:
        for row in range(self._matrix_size):
            for col in range(self._matrix_size):
                matrix[row][col] = random.randint(-9, 9)

    def multiply(self, matrix_a: list = None, matrix_b: list = None) -> list:
        if matrix_a is None:
            matrix_a = self._matrix_a
        if matrix_b is None:
            matrix_b = self._matrix_b
        start = time.time()
        for row in range(self._matrix_size):
            self._calculate_row(matrix_a, matrix_b, row)

        end = time.time()
        print(f"Done in {end - start} sec")

        # for row in range(self.__matrix_size):
        #     print(matrix_a[row], matrix_b[row], self.__result[row])
        # print()
        return self._result

    def _calculate_row(self, matrix_a, matrix_b, row):
        for col in range(self._matrix_size):
            for i in range(self._matrix_size):
                self._result[row][col] += matrix_a[row][i] * matrix_b[i][col]


class MatrixMultipyMultithread(MatrixMultiply):

    def __init__(self,  matrix_size: int = 3) -> None:
        super().__init__(matrix_size)
        self.__barrier: Barrier = Barrier(self._matrix_size + 1)

    def multiply(self, matrix_a: list = None, matrix_b: list = None) -> list:
        if matrix_a is None:
            matrix_a = self._matrix_a
        if matrix_b is None:
            matrix_b = self._matrix_b
        start = time.time()
        for row in range(self._matrix_size):
            Thread(target=self._calculate_row, args=(matrix_a, matrix_b, row)).start()

        self.__barrier.wait()
        end = time.time()
        print(f"Done in {end - start} sec")

        # for row in range(self.__matrix_size):
        #     print(matrix_a[row], matrix_b[row], self.__result[row])
        # print()
        return self._result

    def _calculate_row(self, matrix_a, matrix_b, row):
        super()._calculate_row(matrix_a, matrix_b, row)
        self.__barrier.wait()



if __name__ == "__main__":
    mm1 = MatrixMultiply(1_000)
    mm1.multiply()

    mm2 = MatrixMultipyMultithread(1_000)
    mm2.multiply()
