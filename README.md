# Pi Practice Monitor
*Like a FitBit for (MIDI) keyboard players*

## Goal
A bit of hardware (plus software/firmware, of course) that I can plug into a
MIDI keyboard (via USB) that will monitor my keyboard practice. At a minimum, show
elapsed time for the week's practice. But other interting stats are possible.

## Main Hardware
We need something that can act as a MIDI/USB "host". This seems to be problematic
for anything smaller that a Raspberry Pi Zero. I was hoping to use a Pi Pico or the like,
but USB Host is poorly supported (in CircuitPython anyway). So the first version uses a
Raspberry Pi Zero (Zero2W, to be precise).

## Software
* Full RPi Python code
  * with Adafruit Blinka (see 'Requirements' below)
* <strike>A combination of Python 3.11.x and Bash script (minimal) will do for now.</strike>
* <strike>I'm digging CircuitPython these days, so I hope to stick with that.
  * ISSUE: Blinka (CP s/w for Pi) does not support USB MIDI! See https://docs.circuitpython.org/projects/blinka/en/latest/index.html</strike>
* Also some udev rules & scripts to run it all

## Display
Now using an [Adafruit 1.3: TFT display](https://www.adafruit.com/product/4484) - very nice! 


* Output
 * Usa [Adafruit IoT](https://io.adafruit.com/robcranfill/overview) !
 * Something built-in/on or ? 
 * Could be a web server to a UI, or report data to a server (?)


## Issues
* Power-down safety
 This is the second reason, after cost, that I'd prefer a Pico - how to make it safe to 
 simply power down the device? SOLUTION: Make RPi Linux filesystem read-only.


## To Do
 * LCD display - backlight off doesn't work?
 * Auto-select first MIDI device
 * Handle no MIDI device attached
 * Clear display when done
   * Catch ctrl-C ?

 
## Installation
* Python 3.11.2 used
* Run in a 'venv' - one for PiZero, another for desktop? TODO: needed?
* Python libs
  * (see 'requirements.txt')
* Linux softare
  * RTMIDI backend for Mido
      pip install --pre python-rtmidi
      pip install mido[ports-rtmidi]
      sudo apt-get install libasound2-dev
      sudo apt-get install libjack-dev
 * Adafruit Blinka
as per https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
 * PIL
  * pip install pillow
   * Adafruit Libs
   pip install adafruit-circuitpython-rgb-display

