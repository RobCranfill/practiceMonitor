# Pi Practice Monitor
*Like a FitBit for (MIDI) keyboard players*

## Goal
A bit of hardware (plus software/firmware, of course) that I can plug into a
MIDI keyboard (via USB) that will monitor my keyboard practice. At a minimum, show
elapsed time for the week's practice. But other interesting stats are possible.

First, implement a Minimum Viable Product; add bells and whistles later (what a concept!).

Eventually create a front-end &ndash; app? website? &ndash; to slice and dice the data.
Add social features?


## Main Hardware
We need something that can act as a MIDI/USB "host". This seems to be problematic
for anything smaller than a Raspberry Pi Zero, which is what I'm using now (Zero2W).
I was hoping to use a Pi Pico or the like, but USB Host capability is currently poorly
supported (in CircuitPython anyway). 


## Software
* Full RPi Python (3.11.x) code
  * with Adafruit Blinka (see 'Installation' below) and a bunch of other stuff!
* Also some udev rules & scripts to run it all
* If we ever move to a smaller device, CircuitPython will probably be necessary.


## Display
Now using an [Adafruit 1.3: TFT display](https://www.adafruit.com/product/4484) - looks nice! 
Except it's *slow*! Either find a workaround or find a replacement display. 
My first instance of this part has developed visible defects. Are they fragile? short lived?


## Minimum Viable Product
Need to define this and implement it first! Nothing fancy!!


## Stretch Goals (post MVP)
* Data collection, storage, presentation
 * Use [Adafruit IoT](https://io.adafruit.com/robcranfill/overview) ?
   * Device sends session data updates to cloud
   * Phone/desktop app queries cloud and shows data analysis


## Issues
* Power-down safety
 This is the second reason, after cost, that I'd prefer a Pico - how to make it safe to 
 simply power down the device? 
  * One solution: Make RPi Linux filesystem read-only. See https://learn.adafruit.com/read-only-raspberry-pi
    * Can I make some of it R/W? For persistence? Needed??
  * Workaround: GUI menu for shutdown
 * https://github.com/RobCranfill/practiceMonitor/security/dependabot/1
 * Alternate display 
  
Since the display of the elapsed session time seems problematic (doesn't update nicely) 
can we show something else? Like just a "Session in progress" screen? But that doesn't encourage 
extending a session ("I see I have practiced for 17 minutes - can I make it to 20?").

## Installation
* Python 3.11.2 used
* Runs in a 'venv':
  * <code>python -m venv zenv --system-site-packages</code>
  * <code>source zenv/bin/activate</code>
* Python libs
  * Blinka:
    * <code>pip3 install --upgrade adafruit-python-shell</code>
    * <code>wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py</code>
    * <code>sudo -E env PATH=$PATH python3 raspi-blinka.py</code>
  * <code>sudo apt-get install python-dev</code>
  * <code>pip install -f requirements.txt</code>
* Misc
  * sudo apt-get install fonts-dejavu
  * 
* The following are no longer needed, since we use the above requirements file. Delete after verification!
  <strike>
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
</strike>

## Linux service
* TODO:
  * Use syslog (or whatever)
  * Done:
  * <strike>How to check if service already running? (For running from command line)
    </strike>


* Notes
  * script at /lib/systemd/system/pmz.service
    * <code>sudo chmod 644 /lib/systemd/system/pmz.service</code>
  * <code>sudo systemctl daemon-reload</code>
  * <code>sudo systemctl [enable|disable|start|stop|status] pmz.service</code>


## Workflow Revisited
 * Attach PiZero2W via USB MIDI cable (& OTC connector) to MPKmini; via USB to power brick.
 * Wait until 'ping pizero2w.local' returns a hit.
 * On PC, run './mountsmb.sh' to mount SMB share, start Code pointing to SMB share.
 * Use Termius (or whatever) to SSH to pizero2w.local.
 * On PiZero2w, run 'source zenv/bin/activate' to start venv for PMon.
 * Scripts on pmz:
   * pmz.sh - runs the code in the forground, for development
   * mountsmb.sh - as above
   * check_pm_service.sh - sees if PMon is running in background; bad things happen if you try to run code twice.
   * runPMZ.sh - script that runs the PMon as a service, for running standalone.
     * Document above at "Linux Service"


## To Do
 * USE GITHUB 'ISSUES' FOR THIS.
 * Completed:
   * Handle no MIDI device attached - including displaying msg on LCD
   * Handle SIGTERM/INT &c (blank screen, etc)
   * Show MIDI device name on LCD
   * LCD display - backlight off doesn't work
   * Clear/poweroff display when done
   * Auto-select appropriate MIDI device
   * Create stand-alone command to turn off backlight; use it.
 
