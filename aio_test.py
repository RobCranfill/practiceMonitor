# test of adafruit iot lib
# robcranfill
# sys.arg[1] must be Adafruit AIO API key

import random
import sys
import time

from Adafruit_IO import Client

if len(sys.argv) != 2:
    print("Must provide API key!")
    sys.exit(1)
api_key = sys.argv[1]

# This works for a feed in the "Default" group
FEED_NAME = "perfdata"
# How is this name supposed to be formatted? neither "/" nor "." work.
# FEED_NAME = "PracticeMonitor.perfdata"


def generate_test_data():
    result = []
    t_start = time.time()
    print(f"sess#\tstart\tdur (sec)")
    for i in range(10):
        t_duration = random.randint(60, 600)
        record = f"{i}\t{time.ctime(t_start)}\t{t_duration}"
        print(record)
        t_start += t_duration + random.randint(600, 1200)
        result.append(record)
    return result

def send_data(api_key, data):
    try:
        aio = Client("robcranfill", api_key)
        print("client OK")

        for d in data:
            aio.send(FEED_NAME, d)
        print("send OK")

    except Exception as e:
        print(e)
        print("Ouch!")


d = generate_test_data()
print(f"Data: {d}")

send_data(api_key, d)
