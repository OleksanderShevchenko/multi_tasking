import re
import time
from abc import ABC
from multiprocessing import Process, Queue


class PolygonAreaCalculate(ABC):

    _PTS_REGEX = r"\((\d*),(\d*)\)"
    _MAX_PROCESS = 20

    def __init__(self) -> None:
        super().__init__()
        self._input_queue = Queue(maxsize=1000)  # queue for input strings
        self._output_queue = Queue()  # queue for collecting results

    def _find_area(self) -> None:
        polygon_str = self._input_queue.get()
        line_str = polygon_str
        line_inx = 0
        if polygon_str is not None:
            line_inx, line_str = polygon_str.split("-")
        while polygon_str is not None:
            area = 0
            points = []
            for xy in re.finditer(self._PTS_REGEX, line_str):
                points.append((int(xy.group(1)), int(xy.group(2))))

            for i in range(len(points)):
                a, b = points[i], points[(i + 1) % len(points)]
                area += a[0] * b[1] - a[1] * b[0]  # Shoelace formula of area calculation.
            area = abs(area) / 2.0
            self._output_queue.put(f"{line_inx} - {area}")
            polygon_str = self._input_queue.get()
            line_str = polygon_str
            if polygon_str is not None:
                line_inx, line_str = polygon_str.split("-")

    def calculate_area(self):
        processes = []
        for _ in range(self._MAX_PROCESS):
            p = Process(target=self._find_area, args=())
            processes.append(p)
            p.start()

        with open("polygons.txt", "rt") as fp:
            lines = fp.readlines()
        start = time.time()
        i = 1
        for line in lines:
            self._input_queue.put(f"{i} - {line}")
            i += 1
        for _ in range(self._MAX_PROCESS):
            self._input_queue.put(None)

        for p in processes:
            p.join()
        end = time.time()

        print(f"Done in {end - start} sec.")


if __name__ == "__main__":
    pac = PolygonAreaCalculate()
    pac.calculate_area()
    while not pac._output_queue.empty():
        idx, area = pac._output_queue.get().split("-")
        print(f" Polygon #{idx} area = {area}")