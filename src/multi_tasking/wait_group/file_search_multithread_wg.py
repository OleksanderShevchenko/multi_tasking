import os
import time
from threading import Thread, Lock

from src.multi_tasking.wait_group.wait_group import WaitGroup


class FileSearcher():

    def __init__(self, root_path: str, file_name: str) -> None:
        self._file: str = file_name.lower()
        if os.path.isdir(root_path):
            self._root: str = root_path
        else:
            raise ValueError(f'Inconsistent root directory passed for search - {root_path} ')
        self._matches = []
        self._mutex = Lock()

    def search(self) -> None:
        self._matches.clear()
        wait_group: WaitGroup = WaitGroup()  # using WaitGroup class to wait for all threads

        def __do_search(root: str, file_for_search: str, wait_group: WaitGroup) -> None:
            print(f"Searching in {root} for file with name {file_for_search}")
            for item in os.listdir(root):
                full_path = os.path.join(root, item).lower()
                if os.path.isdir(full_path):  # for new subdirectory create new thread
                    wait_group.add(1)  # add wait count for new thread
                    t = Thread(target=__do_search, args=(full_path, file_for_search, wait_group))
                    t.start()
                if file_for_search in full_path:
                    self._mutex.acquire()
                    self._matches.append(full_path)
                    self._mutex.release()
            wait_group.done()  # done this thread in wait group

        wait_group.add(1)  # add wait count for new thread
        t = Thread(target=__do_search, args=(self._root, self._file, wait_group))
        t.start()  # run first thread
        wait_group.wait()  # wait for all threads


if __name__ == "__main__":
    fs = FileSearcher('<my_directory>', "README.md")
    start = time.perf_counter()
    fs.search()
    end = time.perf_counter()
    i = 1
    for item in fs._matches:
        print(f"#{i} Find matched file {item}")
        i += 1
    print(f"Search takes {end - start} sec.")
