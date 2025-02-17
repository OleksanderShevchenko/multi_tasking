import re
import time
from abc import ABC
from multiprocessing import Process, Queue, current_process, Manager


class PolygonAreaCalculate(ABC):

    _PTS_REGEX = r"\((\d*),(\d*)\)"
    _MAX_PROCESS = 20

    def __init__(self) -> None:
        super().__init__()
        self._input_queue = Queue(maxsize=1000)  # queue for input strings
        self._output_queue = Queue(maxsize=1000)  # queue for collecting results

    def _find_area(self) -> None:
        while True:
            polygon_str = self._input_queue.get()
            if polygon_str is None:
                # print(f"\nProcess {current_process().name} received termination signal.")
                break
            line_inx, line_str = polygon_str.split("-", 1)
            # print(f"\nProcess {current_process().name} processing: line #{line_inx}")
            area = 0
            points = []
            for xy in re.finditer(self._PTS_REGEX, line_str):
                points.append((int(xy.group(1)), int(xy.group(2))))

            for i in range(len(points)):
                a, b = points[i], points[(i + 1) % len(points)]
                area += a[0] * b[1] - a[1] * b[0]  # Shoelace formula of area calculation.
            area = abs(area) / 2.0
            self._output_queue.put(f"{line_inx} - {area}")

    def _consume_output(self, results) -> None:
        while True:
            result = self._output_queue.get()
            if result is None:
                # print(f"\nProcess {current_process().name} received termination signal.")
                break
            idx, area = result.split("-")
            # print(f"\nPolygon #{idx} area = {area}")
            results.append((int(idx), float(area)))

    def calculate_area(self) -> dict:
        result_areas = {}
        with Manager() as manager:
            results = manager.list()  # Shared list to store results
            processes = []
            for _ in range(self._MAX_PROCESS):
                p = Process(target=self._find_area, args=())
                processes.append(p)
                p.start()

            consumer = Process(target=self._consume_output, args=(results,))
            consumer.start()

            with open("polygons.txt", "rt") as fp:
                lines = fp.readlines()

            start = time.time()
            for i, line in enumerate(lines, start=1):
                self._input_queue.put(f"{i} - {line.strip()}")

            # Add termination signals
            for _ in range(self._MAX_PROCESS):
                self._input_queue.put(None)

            for p in processes:
                p.join()
            end = time.time()

            self._output_queue.put(None)
            consumer.join()

            print(f"Done in {end - start} sec.")

            # Access results from the main thread
            for idx, area in results:
                result_areas[f"Polygon #{idx} area ="] = area
        return result_areas


if __name__ == "__main__":
    pac = PolygonAreaCalculate()
    result = pac.calculate_area()
    print(f"Obtain {len(result)} results!")
    for key, value in result.items():
        print(key, value)