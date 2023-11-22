# Pi Practice Monitor
*Like a FitBit for (MIDI) keyboard players*

## Goal
A bit of hardware (plus software/firmware, of course) that I can plug into a
MIDI keyboard (via USB) that will monitor my keyboard practice. At a minimum, show
elapsed time for the week's practice. But other interting stats are possible.

Eventually create a front-end &ndash; app? website? &ndash; to slice and dice the data.


## Main Hardware
We need something that can act as a MIDI/USB "host". This seems to be problematic
for anything smaller than a Raspberry Pi Zero, which is what I'm using now )Zero2W).
I was hoping to use a Pi Pico or the like, but USB Host cap[ability is poorly
supported (in CircuitPython anyway). 


## Software
* Full RPi Python (3.11.x) code
  * with Adafruit Blinka (see 'Requirements' below)
* Also some udev rules & scripts to run it all
* If we ever move to a smaller device, CircuitPython will probably be necessary.


## Display
Now using an [Adafruit 1.3: TFT display](https://www.adafruit.com/product/4484) - looks nice! 
Except it's *slow*! Either find a workaround or find a replacement display.


* Output
 * Use [Adafruit IoT](https://io.adafruit.com/robcranfill/overview) !
   * Device sends session data to cloud
   * Phone/Desktop app queries cloud and shows data analysis


## Issues
* Power-down safety
 This is the second reason, after cost, that I'd prefer a Pico - how to make it safe to 
 simply power down the device? 
   * SOLUTION: Make RPi Linux filesystem read-only. See https://learn.adafruit.com/read-only-raspberry-pi
   * Can I make some of it R/W? For persistence? Needed??


## To Do
 * Handle no MIDI device attached
 * Done:<strike>
   * Handle SIGTERM/INT &c (blank screen, etc)
   * Show MIDI device name on LCD
   * LCD display - backlight off doesn't work
   * Clear display when done
   * Auto-select appropriate MIDI device (HOW?)
   </strike>
 

## Installation
* Python 3.11.2 used
* Run in a 'venv' - one for PiZero <strike>, another for desktop (don't need TK stuff on Pi)</strike>
* Python libs
  * (see 'requirements.txt')
* Linux softare
  * RTMIDI backend for Mido<code>
    * pip install --pre python-rtmidi
    * pip install mido[ports-rtmidi]
    * sudo apt-get install libasound2-dev
    * sudo apt-get install libjack-dev</code>
 * Adafruit Blinka
as per https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
 * PIL
  * pip install pillow
   * Adafruit Libs
     * pip install adafruit-circuitpython-rgb-display
     * IOT (Internet of Things) 
       * <code>pip3 install adafruit-io</code>
       * see https://learn.adafruit.com/welcome-to-adafruit-io/python-and-adafruit-io


## Linux service
* TODO:
  * How to check if service already running? (For running from command line)

* Notes:
  * script at /lib/systemd/system/pmz.service
    * <code>sudo chmod 644 /lib/systemd/system/pmz.service</code>
  * <code>sudo systemctl daemon-reload</code>
  * <code>sudo systemctl [enable|disable|start|stop|status] pmz.service</code>
