import json, random, time
from tqdm import tqdm
from typing import Optional


def read_json(path: str, encoding: Optional[str] = None) -> list | dict:
    return json.load(open(path, encoding=encoding))


def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for _ in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)


with open('keys.txt', 'r') as file:
    accounts = file.read().splitlines()