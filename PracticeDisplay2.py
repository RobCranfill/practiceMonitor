# PracticeDisplay object for MIDIbit project
# robcranfill
# Based on Adafruit code by ladyada

import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
# import displayio


# display shows
#   RUNNING TOTAL TIME    in 48 pt
#   CURRENT SESSION TIME  in 24 pt
#   SESSION NUMBER          "
#   NOTES THIS SESSION      "


FONT_SIZE_BIG   = 48
FONT_SIZE_SMALL = 24


def pretty_time(secs):
    h = 0
    m = int(secs // 60)
    s = int(secs  % 60)
    return (f"{h:02}:{m:02}:{s:02}")

class PracticeDisplay:

    def __init__(self):

        # Configuration for CS and DC pins
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None

        # Config for display baudrate (default max is 24mhz)
        BAUDRATE = 64000000

        # Setup SPI bus using hardware SPI
        spi = board.SPI()

        # Create the ST7789 display
        disp = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
            width=240,
            height=240,
            x_offset=0,
            y_offset=80,
            )
        
        # hang onto this
        self.disp_ = disp

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        height = disp.width  # we swap height/width to rotate it to landscape (huh?)
        width = disp.height
        image = Image.new("RGB", (width, height))
        rotation = 0

        # and these
        self.image_ = image
        self.rotation_ = rotation
        self.height_ = height
        self.width_ = width

        # Get drawing object to draw on image
        draw = ImageDraw.Draw(image)
        self.draw_ = draw
    
        # Draw a black filled box to clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        disp.image(image, rotation)

        # Fonts to use.
        # (Some other nice fonts to try: http://www.dafont.com/bitmap.php)

        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_SMALL)
        self.small_font_ = small_font

        big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_BIG)
        self.big_font_ = big_font

        # Connect to the backlight and turn it on.
        self.backlight_ = digitalio.DigitalInOut(board.D22)
        self.backlight_.switch_to_output()

        self.set_backlight_on(True)

        # end __init__

    def set_backlight_on(self, on_state):
        # print(f"* Setting backlight {on_state}")
        self.backlight_.value = on_state

    def __del__(self):

        # print("* Garbage-collecting display object")

        self.set_backlight_on(False)

        self.disp_ = None
        self.image_ = None
        self.rotation_ = None
        self.height_ = None
        self.width_ = None
        self.big_font_ = None
        self.small_font_ = None
    
        self.backlight_.deinit()
        self.backlight_ = None
        
        # No equivalent in PIL?
        # displayio.release_displays()


    def clear_display(self):
        self.draw_.rectangle((0, 0, self.width_, self.height_), outline=0, fill=(0, 0, 0))
        self.disp_.image(self.image_, self.rotation_)

    def draw_text_in_color(self, line_number, string, color):
        x = 0
        y = line_number * FONT_SIZE_SMALL
        w = self.width_
        h = FONT_SIZE_SMALL

        # black out old text
        # print(f"clearing {x}, {y}, {w}, {y+h}")
        self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

        self.draw_.text((x, y), string, font=self.small_font_, fill=color)
        self.disp_.image(self.image_, self.rotation_)

    def draw_text_in_white(self, line_number, string):
        self.draw_text_in_color(line_number, string, "#FFFFFF")

    # def show_elapsed_time(self, n_seconds):
    #     x = 10
    #     y = 0
    #     w = self.width_
    #     h = FONT_SIZE_BIG

    #     # black out old text
    #     # print(f"showElapsedTime clearing {x}, {y}, {w}, {y+h}")
    #     self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

    #     self.draw_.text((x, y), f"{pretty_time(n_seconds)}", font=self.big_font_, fill="#00FFFF")
    #     self.disp_.image(self.image_, self.rotation_)

    def show_elapsed_time(self, time_str):
        x = 10
        y = 0
        w = self.width_
        h = FONT_SIZE_BIG

        # black out old text
        self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

        self.draw_.text((x, y), time_str, font=self.big_font_, fill="#00FFFF")
        self.disp_.image(self.image_, self.rotation_)

    def show_session_time(self, time_str):
        x = 10
        y = 50
        w = self.width_
        h = FONT_SIZE_BIG

        # black out old text
        self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

        self.draw_.text((x, y), time_str, font=self.big_font_, fill="#00FF00")
        self.disp_.image(self.image_, self.rotation_)


    def set_time_total(self, time_str):
        self.show_elapsed_time(time_str)

    def set_time_session(self, session_str):
        self.show_session_time(session_str)

    def set_time_session_fg(self, fg_color_str):
        print(f"set_time_session_fg {fg_color_str}")

    def set_session_label(self, session_str):
        self.draw_text_in_white(5, session_str)

    def set_notes_label(self, notes_str):
        self.draw_text_in_white(6, notes_str)

    def show_timeout(self, n_timeout):
        self.draw_text_in_color(6, f"Timeout: {n_timeout} sec", "#00FF00")

    def set_status_blob(self, color):
        self.draw_.rectangle((5, 200, 25, 225), outline=0, fill=color)
        self.disp_.image(self.image_, self.rotation_)




def test():
    pd = PracticeDisplay()
    pd.clear_display()
    pd.draw_text_in_color(1, "Hey Cran!",       "#FF0000")
    pd.draw_text_in_color(2, "   what's",       "#00FF00")
    pd.draw_text_in_color(3, "     happening?", "#00FFFF")
    pd.draw_text_in_white(4, " okeedokee??")
    
    print("displaying!")
    # while True:
    #     pass

if __name__ == "__main__":
    test()