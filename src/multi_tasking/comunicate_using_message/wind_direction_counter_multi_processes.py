import os
import re
from multiprocessing.connection import Pipe, Connection
from multiprocessing import Process
from os.path import join

import time

from src.multi_tasking.comunicate_using_message.wind_direction_counter_single_thread import WindDirectionCounter


class WindDirectionCounterMultiProcess(WindDirectionCounter):

    def __init__(self):
        super().__init__()


    def _parse_to_array(self, file_connection_b: Connection, parse_connection_a: Connection) -> None:
        file_content = file_connection_b.recv()
        while file_content is not None:
            lines = file_content.splitlines()
            metar_str = ""
            metars = []  # METeorological Airport ReportS
            for line in lines:
                if re.search(self._TAF_REGEX, line):
                    break
                if not re.search(self._COMMENT_REGEX, line):
                    metar_str += line.strip()
                if re.search(self._METAR_CLOSE_REGEX, line):
                    metars.append(metar_str)
                    metar_str = ""
            parse_connection_a.send(metars)
            file_content = file_connection_b.recv()
        parse_connection_a.send(None)


    def _extract_wind_direction(self, parse_connection_b: Connection, metars_connection_a: Connection) -> None:
        winds = []
        metars = parse_connection_b.recv()
        while metars is not None:
            for metar in metars:
                if re.search(self._WIND_REGEX, metar):
                    for token in metar.split():
                        if re.match(self._WIND_EX_REGEX, token):
                            winds.append(re.match(self._WIND_EX_REGEX, token).group(1))
            metars_connection_a.send(winds)
            metars = parse_connection_b.recv()
        metars_connection_a.send(None)

    def _mine_wind_distribution(self, metars_connection_b: Connection, wind_dist_connection_a: Connection) -> None:
        wind_dist = [0] * 8
        winds = metars_connection_b.recv()
        while winds is not None:
            for wind in winds:
                if re.search(self._VARIABLE_WIND_REGEX, wind):
                    for i in range(8):
                        wind_dist[i] += 1
                elif re.search(self._VALID_WIND_REGEX, wind):
                    d = int(re.match(self._WIND_DIR_ONLY_REGEX, wind).group(1))
                    dir_index = round(d / 45.0) % 8
                    wind_dist[dir_index] += 1
        wind_dist_connection_a.send(wind_dist)

    def process_files(self, path_with_files: str) -> list:
        file_connection_a, file_connection_b = Pipe()
        parse_connection_a, parse_connection_b = Pipe()
        metars_connection_a, metars_connection_b = Pipe()
        wind_dist_connection_a, wind_dist_connection_b = Pipe()
        Process(target=self._parse_to_array, args=(file_connection_b, parse_connection_a)).start()
        Process(target=self._extract_wind_direction, args=(parse_connection_b, metars_connection_a)).start()
        Process(target=self._mine_wind_distribution(metars_connection_b, wind_dist_connection_a)).start()
        for file in os.listdir(path_with_files):
            file_path = join(path_with_files, file)
            if os.path.isfile(file_path):
                with open(file_path, "r") as fp:
                    file_content = fp.read()
                if file_content:
                    file_connection_a.send(file_content)
        file_connection_a.send(None)
        wind_dist = wind_dist_connection_b.recv()
        return wind_dist


if __name__ == '__main__':
    path_with_files = "../metarfiles"
    parser = WindDirectionCounter()
    start = time.time()
    wind_dist = parser.process_files(path_with_files)
    end = time.time()
    print(wind_dist)
    print("Time taken", end - start)