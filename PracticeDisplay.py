# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

class PracticeDisplay:

    def __init__(self):

        # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None

        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 64000000

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        # Create the ST7789 display:
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
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
        image = Image.new("RGB", (width, height))
        rotation = 180

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

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = height - padding

        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the
        # same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        self.font_ = font

        # Turn on the backlight
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True

        # end __init__

    def clear_display(self):
        self.draw_.rectangle((0, 0, self.width_, self.height_), outline=0, fill=(0, 0, 0))
        self.disp_.image(self.image_, self.rotation_)

    def draw_line_color(self, line_number, string, color):
        x =  0
        y = line_number * 24
        h = 24
        w = self.font_.getlength(string)

        # black out old text
        # print("clearing {x}, {y}, {h}, {w}")
        self.draw_.rectangle((0, 0, w, h), outline=0, fill=0)

        self.draw_.text((x, y), string, font=self.font_, fill=color)
        self.disp_.image(self.image_, self.rotation_)

    def draw_line_black(self, line_number, string):
        draw_line_color(self, line_number, string, "#FFFFFF")

def test():
    pd = PracticeDisplay()
    pd.clear_display()
    pd.draw_line_color(1, "Hey Cran!",       "#FF0000")
    pd.draw_line_color(2, "   what's",       "#00FF00")
    pd.draw_line_color(3, "     happening?", "#00FFFF")
    
    print("displaying????")
    # while True:
    #     pass

if __name__ == "__main__":
    test()