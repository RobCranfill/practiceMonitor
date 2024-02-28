# For the Adafruit miniPiTFT 3.3" LCD display, turn on/off (mostly off) the backlight
# robcranfill

import board
import digitalio
import sys

def set_backlight_state(backlight_on: bool) -> None:
    backlight_ = digitalio.DigitalInOut(board.D22)
    backlight_.switch_to_output()
    backlight_.value = backlight_on


if __name__ == "__main__":

    yeses = ["on", "yes", "1"]
    nos   = ["off", "no", "0"]
    usage = str(yeses) + " | " + str(nos)
    
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} {usage}")
        sys.exit(1)

    if sys.argv[1].lower() in yeses:
        set_backlight_state(True)
        sys.exit(0)

    if sys.argv[1].lower() in nos:
        set_backlight_state(False)
        sys.exit(0)

    print(f"Usage: {sys.argv[0]} {usage}")
    sys.exit(1)
