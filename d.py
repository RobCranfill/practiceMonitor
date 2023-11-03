# read output from midi util, do something with it
# this is standard Python, not CircuitPython (unfortunately!)

import sys
import time

import PracticeDisplay

NO_ACTIVITY_TIMEOUT_SEC = 10
DISPLAY_LINE_SESSION_TIME   = 1
DISPLAY_LINE_SESSIONS       = 2
DISPLAY_LINE_TIMEOUT        = 3

time_last = 0
total_practice_time = 0
session_count = 0

display = PracticeDisplay.PracticeDisplay()

def pretty_time(secs):
    m = int(secs//60)
    s = int(secs %60)
    return (f"{m}:{s:02}")

display.clear_display()
display.draw_line_white(DISPLAY_LINE_TIMEOUT, f"Timeout: {NO_ACTIVITY_TIMEOUT_SEC} seconds")

# main loop

for line in sys.stdin:
    line_read = line.rstrip().lstrip()
    time_sec = time.time()
    time_delta = time_sec - time_last
    # print(f"Input: '{line_read}' at {time_sec}")
    if time_delta < NO_ACTIVITY_TIMEOUT_SEC:
        total_practice_time += time_delta
        display.draw_line_white(
            DISPLAY_LINE_SESSION_TIME, 
            f"Elapsed: {pretty_time(total_practice_time)}")

    else:
        session_count += 1
        display.draw_line_white(DISPLAY_LINE_SESSIONS, f"Session #{session_count}")
    time_last = time_sec

