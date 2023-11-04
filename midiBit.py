# MIDI-bit - a FitBit for MIDI keyboards
# robcranfill
# 

import select
import sys
import time
import digitalio
import board

import PracticeDisplay2 as PracticeDisplay


NO_ACTIVITY_TIMEOUT_SEC = 10
READ_DELAY_SEC = 0.1


time_last = 0
total_practice_time = 0
session_count = 0

display = PracticeDisplay.PracticeDisplay()



def setup_buttons():
    buttonA = digitalio.DigitalInOut(board.D23)
    buttonB = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB.switch_to_input()
    return buttonA, buttonB

display.clear_display()
display.showElapsedTime(total_practice_time)
display.showSessionNumber(session_count)
display.showTimeout(NO_ACTIVITY_TIMEOUT_SEC)

button_A, button_B = setup_buttons()
button_A_pushed = not button_A.value
button_B_pushed = not button_B.value

# new main loop
line = ""
button_A_was_pushed = button_A_pushed

while True:
  try:
    if select.select([sys.stdin,], [], [], 0)[0]:
      thisChar = sys.stdin.read(1)

      # if it's a newline, process it (could do char-by-char?)
      if thisChar == '\n':
        time_sec = time.time()
        time_delta = time_sec - time_last
        print(f"READ: '{line}'")

        if time_delta < NO_ACTIVITY_TIMEOUT_SEC:
            total_practice_time += time_delta
            display.showElapsedTime(total_practice_time)
        else:
            session_count += 1
            display.showSessionNumber(session_count)

        time_last = time_sec
        line = ""
      else:
        line += thisChar
        # print(f" added '{thisChar}'; line now '{line}'")
    else:
      # print("nothing to read")
      time.sleep(READ_DELAY_SEC)

    # 'select' had nothing. check other things.
    button_A_pushed = not button_A.value
    if button_A_pushed and not button_A_was_pushed:
        print("BUTTON A PRESSED!")
        button_A_was_pushed = button_A_pushed

  except IOError:
    print("io error!")
    pass


# # main loop
# for line in sys.stdin:
#     line_read = line.rstrip().lstrip()
#     time_sec = time.time()
#     time_delta = time_sec - time_last
#     # print(f"Input: '{line_read}' at {time_sec}")
#     if time_delta < NO_ACTIVITY_TIMEOUT_SEC:
#         total_practice_time += time_delta
#         display.showElapsedTime(total_practice_time)
#     else:
#         session_count += 1
#         display.showSessionNumber(session_count)
#     time_last = time_sec
#     print(f"button {button_a.value}")
    
