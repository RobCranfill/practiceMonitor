# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
    Test display code for Adafruit miniPiTFT 1.3" 240x240 on a Raspberry Pi Zero2W
    Why does it take 0.6 seconds to display?

    Based on https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-usage
"""

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789 


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs = cs_pin,
    dc = dc_pin,
    rst = reset_pin,
    baudrate = BAUDRATE,
    width = 240,
    height = 240,
    x_offset = 0,
    y_offset = 80,
    )


# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

# First define some constants to allow easy positioning of text.
padding = -2
x = 0

# Load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

i = 0
y = padding

while True:

    i += 1
    # msg = f"#{i} delta = {(time.time() - t):0.2f}"
    # print(msg)
    # t = time.time()
    
    msg = f"Hello #{i}, Montana!"

    # Draw a black filled box to clear the image
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, y), msg, font=font, fill="#FFFFFF")
    draw.text((x, y+22), msg, font=font, fill="#FF0000")
    draw.text((x, y+44), msg, font=font, fill="#00FF00")
    draw.text((x, y+66), msg, font=font, fill="#0000FF")

    # Display the image
    t2 = time.time()
    disp.image(image)
    print(f"  t2 = {(time.time() - t2):0.2f}")

    # time.sleep(0.1)
