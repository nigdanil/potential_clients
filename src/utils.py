# src/utils.py

import random
import time

def sleep_random(min_sec: int, max_sec: int):
    delay = random.uniform(min_sec, max_sec)
    print(f"🕒 Ожидание {delay:.2f} секунд (имитация человека)...")
    time.sleep(delay)
