import re
import time
from abc import ABC


class PolygonAreaCalculate(ABC):

    _PTS_REGEX = r"\((\d*),(\d*)\)"

    def __init__(self) -> None:
        super().__init__()

    def find_area(self, polygon_str: str) -> float:
        area = 0
        points = []
        for xy in re.finditer(self._PTS_REGEX, polygon_str):
            points.append((int(xy.group(1)), int(xy.group(2))))

        for i in range(len(points)):
            a, b = points[i], points[(i + 1) % len(points)]
            area += a[0] * b[1] - a[1] * b[0]  # Shoelace formula of area calculation.
        return abs(area) / 2.0


if __name__ == "__main__":
    pac = PolygonAreaCalculate()
    areas = []
    with open("polygons.txt", "rt") as fp:
        lines = fp.readlines()
    start = time.time()
    for line in lines:
        areas.append(pac.find_area(line))
    end = time.time()
    i = 1
    for area in areas:
        print(f" Polygon #{i} area = {area}")
        i += 1
    print(f"Done in {end - start} sec.")