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

def setup_buttons():
    buttonA = digitalio.DigitalInOut(board.D23)
    buttonB = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB.switch_to_input()
    return buttonA, buttonB


time_last = 0
total_practice_time = 0
session_count = 0

display = PracticeDisplay.PracticeDisplay()
display.clear_display()
display.show_elapsed_time(total_practice_time)
display.show_session_number(session_count)
display.show_timeout(NO_ACTIVITY_TIMEOUT_SEC)

button_A, button_B = setup_buttons()
button_A_pushed = not button_A.value
button_B_pushed = not button_B.value

led_status = False
led_idle_ticks = 0

line = ""
button_A_was_pushed = button_A_pushed

# main loop
#
while True:
  try:
    if select.select([sys.stdin,], [], [], 0)[0]:
      thisChar = sys.stdin.read(1)

      # if it's a newline, handle the MIDI event (which is to say, notice it)
      # FIXME: we don't really do anything with the string we read, so why build it?
      #
      if thisChar == '\n':
        time_sec = time.time()
        time_delta = time_sec - time_last
        # print(f"read line: '{line}'")

        led_status = not led_status
        display.set_status_blob(("#FF0000" if led_status else "#00FF00"))

        if time_delta < NO_ACTIVITY_TIMEOUT_SEC:
            total_practice_time += time_delta
            display.show_elapsed_time(total_practice_time)
        else:
            session_count += 1
            display.show_session_number(session_count)

        time_last = time_sec
        line = ""
      else:
        line += thisChar
        # print(f" added '{thisChar}'; line now '{line}'")
    else:
      # print("nothing to read")
      time.sleep(READ_DELAY_SEC)

    led_idle_ticks += 1
    if led_idle_ticks > 10:
        display.set_status_blob("#000000")
        led_idle_ticks = 0

    # 'select' had nothing. check other things.
    button_A_pushed = not button_A.value
    if button_A_pushed and not button_A_was_pushed:
        print("BUTTON A PRESSED!")
        button_A_was_pushed = button_A_pushed

  except KeyboardInterrupt:
     print("Done!")
     display.clear_display()
     display = None
     sys.exit(1)

  except IOError:
    print("io error!")
    pass

