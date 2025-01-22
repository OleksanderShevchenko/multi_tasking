import json
from threading import Thread
from urllib import request, error
import time

_counter = 0


def count_letters(url: str, frequency: dict) -> None:
    try:
        response = request.urlopen(url)
    except error.HTTPError as err:
        print(f"\nurl={url} error: {err}")
    else:
        txt = str(response.read())
        for l in txt:
            letter = l.lower()
            if letter in frequency.keys():
                frequency[letter] += 1
    finally:
        global _counter
        _counter += 1


def main() -> None:
    frequency = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    start = time.perf_counter()
    for i in range(1000, 1182):
        url = f"https://www.rfc-editor.org/rfc/rfc{i}.txt"
        Thread(target=count_letters, args=(url, frequency)).start()
    while _counter < 182:
        time.sleep(0.5)
    end = time.perf_counter()
    print(json.dumps(frequency, indent=4))
    print(f"Done in {end - start} seconds")


if __name__ == "__main__":
    main()
