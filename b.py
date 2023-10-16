# read output from midi util, do something with it

import sys
import time

NO_ACTIVITY_TIMEOUT_SEC = 10

time_last = 0
total_practice_time = 0

def pretty(secs):
    m = int(secs//60)
    s = int(secs %60)
    return (f"{m}:{s:02}")

print(f"Timeout is {NO_ACTIVITY_TIMEOUT_SEC}")

for line in sys.stdin:
    line_read = line.rstrip().lstrip()
    time_sec = time.time()
    time_delta = time_sec - time_last
    # print(f"Input: '{line_read}' at {time_sec}")
    if time_delta < NO_ACTIVITY_TIMEOUT_SEC:
        total_practice_time += time_delta
        print(f" total: {pretty(total_practice_time)}")
    time_last = time_sec

