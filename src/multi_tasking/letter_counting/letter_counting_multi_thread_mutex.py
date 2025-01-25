import json
from threading import Thread, Lock
from urllib import request, error
import time

_counter = 0  # variable that represent global shared memory


def count_letters(url: str, frequency: dict, _mutex: Lock) -> None:
    try:
        response = request.urlopen(url)
        txt = str(response.read()).lower()
    except error.HTTPError as err:
        print(f"\nurl={url} error: {err}")
    else:
        _mutex.acquire()
        for letter in txt:
            if letter in frequency.keys():
                frequency[letter] += 1
        _mutex.release()
    finally:
        _mutex.acquire()
        global _counter
        _counter += 1
        _mutex.release()


def main() -> None:
    frequency = {}  # variable that represent local shared memory
    _mutex = Lock()
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    start = time.perf_counter()
    for i in range(1000, 1182):
        url = f"https://www.rfc-editor.org/rfc/rfc{i}.txt"
        Thread(target=count_letters, args=(url, frequency, _mutex)).start()
    while True:
        _mutex.acquire()
        global _counter
        if _counter == 182:
            break
        _mutex.release()
        time.sleep(0.5)
    end = time.perf_counter()
    print(json.dumps(frequency, indent=4))
    print(f"Done in {end - start} seconds")


if __name__ == "__main__":
    main()
