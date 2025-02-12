import os
import re
from abc import ABC
from os.path import join

import time

class WindDirectionCounter(ABC):

    _WIND_REGEX = r"\d* METAR.*EGLL \d*Z [A-Z ]*(\d{5}KT|VRB\d{2}KT).*="
    _WIND_EX_REGEX = r"(\d{5}KT|VRB\d{2}KT)"
    _VARIABLE_WIND_REGEX = r".*VRB\d{2}KT"
    _VALID_WIND_REGEX = r"\d{5}KT"
    _WIND_DIR_ONLY_REGEX = r"(\d{3})\d{2}KT"
    _TAF_REGEX = r".*TAF.*"
    _COMMENT_REGEX = r"\w*#.*"
    _METAR_CLOSE_REGEX = r".*="

    def __init__(self):
        super().__init__()


    def _parse_to_array(self, file_content: str):
        lines = file_content.splitlines()
        metar_str = ""
        metars = []
        for line in lines:
            if re.search(self._TAF_REGEX, line):
                break
            if not re.search(self._COMMENT_REGEX, line):
                metar_str += line.strip()
            if re.search(self._METAR_CLOSE_REGEX, line):
                metars.append(metar_str)
                metar_str = ""
        return metars


    def _extract_wind_direction(self, metars):
        winds = []
        for metar in metars:
            if re.search(self._WIND_REGEX, metar):
                for token in metar.split():
                    if re.match(self._WIND_EX_REGEX, token): winds.append(re.match(self._WIND_EX_REGEX, token).group(1))
        return winds


    def _mine_wind_distribution(self, winds, wind_dist):
        for wind in winds:
            if re.search(self._VARIABLE_WIND_REGEX, wind):
                for i in range(8):
                    wind_dist[i] += 1
            elif re.search(self._VALID_WIND_REGEX, wind):
                d = int(re.match(self._WIND_DIR_ONLY_REGEX, wind).group(1))
                dir_index = round(d / 45.0) % 8
                wind_dist[dir_index] += 1
        return wind_dist

    def process_files(self, path_with_files: str) -> list:
        wind_dist = [0] * 8
        for file in os.listdir(path_with_files):
            file_path = join(path_with_files, file)
            if os.path.isfile(file_path):
                with open(file_path, "r") as fp:
                    file_content = fp.read()
                if file_content:
                    metars = self._parse_to_array(file_content)
                    winds = self._extract_wind_direction(metars)
                    wind_dist = self._mine_wind_distribution(winds, wind_dist)

        return wind_dist


if __name__ == '__main__':
    path_with_files = "../metarfiles"
    parser = WindDirectionCounter()
    start = time.time()
    wind_dist = parser.process_files(path_with_files)
    end = time.time()
    print(wind_dist)
    print("Time taken", end - start)