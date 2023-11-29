# Notes for practive monitor udev rules

## Notes
Goal: write a udev rule &c that notices a MIDI keyboard being plugged in,
and notify the PerfMon app to re-scan the MIDI devices.

## Implementation

### Issues
* How to install this?
* How to install with correct paths?
  * udev rule path to scripts
* Process control:
  * <code>pkill --signal USR1 --full pmZero.py</code>

## What's where

working in <tt>/home/rob/proj/practiceMonitor/udev</tt>
  - <tt>monitor.sh</tt> - test code to watch log file
  - <tt>trigger.sh</tt> - script udev rule will run
  - <tt>/etc/udev/rules.d/88-perfmon.rules</tt> - our udev rule(s)

## testing

Results from test:

### remove
<pre>
Wed Nov 29 09:39:56 PST 2023; usbmisc; remove
Wed Nov 29 09:39:56 PST 2023; snd_seq; remove
Wed Nov 29 09:39:56 PST 2023; usb; unbind
Wed Nov 29 09:39:56 PST 2023; hidraw; remove
Wed Nov 29 09:39:56 PST 2023; sound; remove
Wed Nov 29 09:39:56 PST 2023; sound; remove
Wed Nov 29 09:39:56 PST 2023; sound; remove
Wed Nov 29 09:39:56 PST 2023; sound; remove
Wed Nov 29 09:39:56 PST 2023; usb; remove
Wed Nov 29 09:39:56 PST 2023; hid; unbind
Wed Nov 29 09:39:56 PST 2023; sound; remove
Wed Nov 29 09:39:56 PST 2023; hid; remove
Wed Nov 29 09:39:56 PST 2023; usb; unbind
Wed Nov 29 09:39:56 PST 2023; usb; unbind
Wed Nov 29 09:39:56 PST 2023; usb; remove
Wed Nov 29 09:39:57 PST 2023; usb; remove
Wed Nov 29 09:39:57 PST 2023; usb; unbind
Wed Nov 29 09:39:57 PST 2023; usb; remove
</pre>

### add
More than one call interleaved??? happens on 'remove', too!
<pre>
Wed Nov 29 09:40:21 PST 2023; usb; add
Wed Nov 29 09:40:21 PST 2023Wed Nov 29 09:40:21 PST 2023; usb; add
; usb; add
Wed Nov 29 09:40:21 PST 2023; usb; add
Wed Nov 29 09:40:21 PST 2023; hid; add
Wed Nov 29 09:40:21 PST 2023Wed Nov 29 09:40:21 PST 2023; usbmisc; add
; sound; add
Wed Nov 29 09:40:21 PST 2023; usb; bind
Wed Nov 29 09:40:21 PST 2023; sound; add
Wed Nov 29 09:40:21 PST 2023; sound; add
Wed Nov 29 09:40:21 PST 2023Wed Nov 29 09:40:21 PST 2023; sound; add
; snd_seq; add
Wed Nov 29 09:40:21 PST 2023; hidraw; add
Wed Nov 29 09:40:21 PST 2023; sound; add
Wed Nov 29 09:40:21 PST 2023; hid; bind
Wed Nov 29 09:40:21 PST 2023; usb; bind
Wed Nov 29 09:40:21 PST 2023; usb; bind
Wed Nov 29 09:40:21 PST 2023; usb; bind
Wed Nov 29 09:40:21 PST 2023; sound; change
</pre>


## udevadm
not really that necessary!
<pre>
(zenv) rob@pizero2w:~/proj/practiceMonitor/udev $ udevadm --help

udevadm [--help] [--version] [--debug] COMMAND [COMMAND OPTIONS]

Send control commands or test the device manager.

Commands:
  info          Query sysfs or the udev database
  trigger       Request events from the kernel
  settle        Wait for pending udev events
  control       Control the udev daemon
  monitor       Listen to kernel and udev events
  test          Test an event run
  test-builtin  Test a built-in command
  wait          Wait for device or device symlink
  lock          Lock a block device

See the udevadm(8) man page for details.
</pre>

from <code>journalctl -f -n 0</code>

<pre>
Nov 29 10:45:16 pizero2w kernel: usb 1-1: USB disconnect, device number 24
Nov 29 10:45:18 pizero2w kernel: usb 1-1: new full-speed USB device number 25 using dwc2
Nov 29 10:45:18 pizero2w kernel: usb 1-1: New USB device found, idVendor=2011, idProduct=0715, bcdDevice= 0.00
Nov 29 10:45:18 pizero2w kernel: usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Nov 29 10:45:18 pizero2w kernel: usb 1-1: Product: MPKmini2
Nov 29 10:45:18 pizero2w kernel: usb 1-1: Manufacturer: AKAI
Nov 29 10:45:18 pizero2w kernel: usb 1-1: SerialNumber: 0001
Nov 29 10:45:18 pizero2w kernel: hid-generic 0003:2011:0715.0018: hiddev96,hidraw0: USB HID v1.11 Device [AKAI MPKmini2] on usb-3f980000.usb-1/input0
Nov 29 10:45:18 pizero2w mtp-probe[3480]: checking bus 1, device 25: "/sys/devices/platform/soc/3f980000.usb/usb1/1-1"
Nov 29 10:45:18 pizero2w mtp-probe[3480]: bus: 1, device: 25 was not an MTP device
Nov 29 10:45:18 pizero2w mtp-probe[3502]: checking bus 1, device 25: "/sys/devices/platform/soc/3f980000.usb/usb1/1-1"
Nov 29 10:45:18 pizero2w mtp-probe[3502]: bus: 1, device: 25 was not an MTP device
Nov 29 10:45:18 pizero2w echo[3505]: cran: Sending USR1 signal to pmZero.py
Nov 29 10:45:18 pizero2w (udev-worker)[3455]: card0: Process '/home/rob/proj/practiceMonitor/udev/trigger.sh' failed with exit code 1.
</pre>
