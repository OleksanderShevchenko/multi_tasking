import json
from urllib import request, error
import time


def count_letters(url: str, frequency: dict) -> None:
    try:
        response = request.urlopen(url)
    except error.HTTPError as err:
        print(f"url={url} error: {err}")  # print failed url and error
    else:
        txt = str(response.read())
        for l in txt:
            letter = l.lower()
            if letter in frequency.keys():
                frequency[letter] += 1


def main() -> None:
    frequency = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        frequency[c] = 0
    start = time.perf_counter()
    for i in range(1000, 1182):
        url = f"https://www.rfc-editor.org/rfc/rfc{i}.txt"
        count_letters(url, frequency)
    end = time.perf_counter()
    print(json.dumps(frequency, indent=4))
    print(f"Done in {end - start} seconds")


if __name__ == "__main__":
    main()
