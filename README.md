# Pi Practice Monitor
*Like a FitBit for (MIDI) keyboard players*

## Goal
A bit of hardware (plus software/firmware, of course) that I can plug into a
MIDI keyboard (via USB) that will monitor my keyboard practice. At a minimum, show
elapsed time for the week's practice. But other interting stats are possible.

## Main Hardware
We need something that can act as a MIDI/USB "host". This seems to be problematic
for anything smaller that a Raspberry Pi Zero. I was hoping to use a Pi Pico or the like,
but USB Host is poorly supported (in CircuitPython anyway).

## Software
I'm digging CircuitPython these days, so I hope to stick with that.
* ISSUE: Blinka (CP s/w for Pi) does not support USB MIDI! See https://docs.circuitpython.org/projects/blinka/en/latest/index.html

## Display
Something built-in/on or ? Could be a web server to a UI - on my phone? - or report data to a server.
For now, use a simple Pi display (via I2C?) of some sort.

## Issues
* Power-down safety
 This is the second reason, after cost, that I'd prefer a Pico - how to make it safe to 
 simply power down the device? SOLUTION: Make filesystem read-only.

