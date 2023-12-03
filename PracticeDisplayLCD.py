# PracticeDisplay object for MIDIbit project
# robcranfill
# Based on Adafruit code by ladyada, but repainting only when needed

import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import RPi.GPIO as GPIO



# Display:
#
#   CURRENT SESSION TIME  in big font
#   RUNNING TOTAL TIME    in big font
#   SESSION NUMBER        in small font
#   NOTES THIS SESSION    in small font
#
#
#   Device name           small


FONT_SIZE_BIG   = 48
FONT_SIZE_SMALL = 24

ELAPSED_TIME_Y = 50
SESSION_TIME_Y = 00


REGULAR_COLOR   = "#FFFFFF"
HIGHLIGHT_COLOR = "#FF0000"

WIDGET_AREA_WIDTH  =  30
WIDGET_EXECUTE_Y   =  50
WIDGET_MOVE_Y      = 150
HEADER_AREA_HEIGHT =  24

MAX_MENU_ITEMS = 9


def format_seconds(n_seconds):
    return f"00:{(n_seconds // 60):02}:{(n_seconds % 60):02}"


class PracticeDisplay:

    def __init__(self):

        # Configuration for CS and DC pins
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None

        # Display baudrate (default max is 24mhz)
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
        
        # hang onto this...
        self.disp_ = disp

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        height = disp.width  # we swap height/width to rotate it to landscape (huh?)
        width  = disp.height
        image = Image.new("RGB", (width, height))
        rotation = 0

        # ...and these
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

        # small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_SMALL)
        small_font = ImageFont.load_default(size=FONT_SIZE_SMALL)
        self.small_font_ = small_font

        # big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_BIG)
        big_font = ImageFont.load_default(size=FONT_SIZE_BIG)
        self.big_font_ = big_font

        # Connect to the backlight and turn it on.
        self.backlight_ = digitalio.DigitalInOut(board.D22)
        self.backlight_.switch_to_output()

        self.set_backlight_on(True)

        # end __init__


    def show_image(self, image_path):

        self.draw_.rectangle((0, 0, self.width_, self.height_), outline=0, fill=(0, 0, 0))
        self.disp_.image(self.image_)

        new_image = Image.open(image_path)

        # Scale the image to the smaller screen dimension
        image_ratio = new_image.width / new_image.height
        screen_ratio = self.width_ / self.height_
        if screen_ratio < image_ratio:
            scaled_width = new_image.width * self.height_ // new_image.height
            scaled_height = self.height_
        else:
            scaled_width = self.width_
            scaled_height = new_image.height * self.width_ // new_image.width
        new_image = new_image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - self.width_ // 2
        y = scaled_height // 2 - self.height_ // 2
        new_image = new_image.crop((x, y, x + self.width_, y + self.height_))

        # Display image.
        self.disp_.image(new_image)


    def set_backlight_on(self, on_state):
        print(f"* Setting backlight {'on' if on_state else 'off'}")
        self.backlight_.value = on_state

    def __del__(self):

        print("* Garbage-collecting display object")

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
        

    def clear_display(self):
        self.draw_.rectangle((0, 0, self.width_, self.height_), outline=0, fill=(0, 0, 0))
        self.disp_.image(self.image_, self.rotation_)


    # paint all the changes that have been made
    def update_display(self):

        # FIXME: This takes 0.6 seconds!

        # start = time.time()
        self.disp_.image(self.image_, self.rotation_)
        # print(f"update_display: {(time.time() - start):0.2f} s")


    def draw_text_in_color(self, line_number, string, color):

        start = time.time()

        x = 0
        y = line_number * FONT_SIZE_SMALL
        w = self.width_
        h = FONT_SIZE_SMALL

        # black out old text
        # print(f"clearing {x}, {y}, {w}, {y+h}")
        self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

        self.draw_.text((x, y), string, font=self.small_font_, fill=color)
        # self.disp_.image(self.image_, self.rotation_)

        # print(f"draw_text_in_color: {(time.time() - start):0.2f} s")


    def draw_text_in_white(self, line_number, string):
        self.draw_text_in_color(line_number, string, "#FFFFFF")


    def show_elapsed_time(self, n_seconds):
        x = 10
        y = ELAPSED_TIME_Y
        w = self.width_
        h = FONT_SIZE_BIG

        # black out old text
        self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

        self.draw_.text((x, y), format_seconds(n_seconds), font=self.big_font_, fill="#00FFFF")
        # self.disp_.image(self.image_, self.rotation_)


    def show_session_time(self, n_seconds):
        x = 10
        y = SESSION_TIME_Y
        w = self.width_
        h = FONT_SIZE_BIG

        # black out old text
        self.draw_.rectangle((0, y, w, y+h), outline=0, fill="#000000")

        self.draw_.text((x, y), format_seconds(n_seconds), font=self.big_font_, fill="#00FF00")
        # self.disp_.image(self.image_, self.rotation_)


    # def set_time_total(self, time_str):
    #     self.show_elapsed_time(time_str)

    # def set_time_session(self, session_str):
    #     self.show_session_time(session_str)

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
        # self.disp_.image(self.image_, self.rotation_)

    def set_device_name(self, device_str):
        self.draw_text_in_color(9, device_str, "#00FF00")



# ************************************************** NEW MENU STUFF
    def start_menu_mode(self, menu_data):
        self.menu_data = menu_data
        self.menu_item_selected = 0
        self.clear_display()
        self.update_menu_display()

    def select_next_item(self):
        self.menu_item_selected = (self.menu_item_selected + 1) % len(self.menu_data)
        self.update_menu_display()

    def select_prev_item(self):
        self.menu_item_selected = (self.menu_item_selected -1) % len(self.menu_data)
        self.update_menu_display()

    def update_menu_display(self):
        i = 0
        for m in self.menu_data:
            c = "#00FF00" if i == self.menu_item_selected else "#FFFFFF"
            self.draw_text_in_color(i, m["text"], c)
            i += 1


def test():
    print("\nRunning test code for PracticeDisplay....")

    pd = PracticeDisplay()
    pd.clear_display()
    pd.draw_text_in_color(1, "Hey Cran!",       "#FF0000")
    pd.draw_text_in_color(2, "   what's",       "#00FF00")
    pd.draw_text_in_color(3, "     happening?", "#00FFFF")
    pd.draw_text_in_white(4, " okeedokee??")
    
    print("Displaying! Press ^C to break")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nCleaning up...")
        pd = None

if __name__ == "__main__":
    test()