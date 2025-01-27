import os


class FileSearcher():

    def __init__(self, root_path: str, file_name: str) -> None:
        self._file: str = file_name.lower()
        if os.path.isdir(root_path):
            self._root: str = root_path
        else:
            raise ValueError(f'Inconsistent root directory passed for search - {root_path} ')
        self._matches = []

    def search(self) -> None:
        self._matches.clear()

        def __do_search(root: str, file_for_search: str) -> None:
            print(f"Searching in {root} for file with name {file_for_search}")
            for item in os.listdir(root):
                full_path = os.path.join(root, item).lower()
                if os.path.isdir(full_path):
                    __do_search(full_path, file_for_search)
                if file_for_search in full_path:
                    self._matches.append(full_path)

        __do_search(self._root, self._file)


if __name__ == "__main__":
    fs = FileSearcher('D:\\Shevchenko\\Work', "README.md")
    fs.search()
    i = 1
    for item in fs._matches:
        print(f"#{i} Find matched file {item}")
        i += 1
