# MIDI-bit - a FitBit for MIDI keyboards
# robcranfill
# 

import sys
import time

import PracticeDisplay2 as PracticeDisplay


NO_ACTIVITY_TIMEOUT_SEC = 10

time_last = 0
total_practice_time = 0
session_count = 0

display = PracticeDisplay.PracticeDisplay()

display.clear_display()
display.showElapsedTime(total_practice_time)
display.showSessionNumber(session_count)
display.showTimeout(NO_ACTIVITY_TIMEOUT_SEC)

# main loop
for line in sys.stdin:
    line_read = line.rstrip().lstrip()
    time_sec = time.time()
    time_delta = time_sec - time_last
    # print(f"Input: '{line_read}' at {time_sec}")
    if time_delta < NO_ACTIVITY_TIMEOUT_SEC:
        total_practice_time += time_delta
        display.showElapsedTime(total_practice_time)

    else:
        session_count += 1
        display.showSessionNumber(session_count)
    time_last = time_sec

