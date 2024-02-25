# Notes for Practice Monitor udev rules

## Purpose
The Python code that uses the <b>mido</b> library doesn't seem to be able
to tell that a keyboard has been disconnected (usually by being turned off).
We need a way to notify the app that things have changed.

## Implementation
Via the <tt>udev</tt> facility, watch for an appropriate device (what?) being added (removed? changed?)
and run a script that sends a signal to the Python code to re-scan the MIDI devices.

Currently we catch all USB "ACTION=change" actions. This was nice because in testing I only saw one "change"
for any given physical plugging-in, as opposed to multiple "add" and "bind" actions.

(Whereas "ACTION=add" and "ACTION=remove" each cause 13 udev events!)

*But* this does not catch removal of the device, hence the outstanding issue (#7) of not being able to show that in the GUI.

This still probably fires more often than needed (for other devices than keyboards) but works.
It would be better to only do so with appropriate devices ("sound"? "alsa"?). 
[See note below re: seeing a different udevv action on my laptop.]

The trigger script sends a USR1 signal to the Python code, which is found via the <tt>pkill</tt> command.


# Installation
* Copy udev file <tt>10-pracmon.rules</tt> to <tt>/etc/udev/rules.d/</tt>

### Issues
* There's a full path to the shell script in my <tt>home</tt> dir in the udev rule. Ugly but OK.


## What's where
Working dir <tt>/home/rob/proj/practiceMonitor/udev</tt>
  - <tt>trigger.sh</tt> - script udev rule will run


## Notes
* https://www.reactivated.net/writing_udev_rules.html#external-run was very helpful writing udev rules, if a little out of date.
* To see messages from shell script, <code>journalctl -f -n 0</code>
  * Or <code>journalctl -f -n 0 | grep pracmon</code> to see just our messages.

  
## Notes from testing

### udevadm messages whilst un/plugging keyboard


Note that the following was performed on my laptop, not the PiZero, and does
not show a "change" event! Possible issue for a desktop version.

<code>udevadm monitor --subsystem-match=usb</code>
<pre>
rob@robuntuflex:~/proj/practiceMonitor/udev$ udevadm monitor --subsystem-match=usb
monitor will print the received events for:
UDEV - the event which udev sends out after rule processing
KERNEL - the kernel uevent

KERNEL[2320.869236] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
KERNEL[2320.869390] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
KERNEL[2320.870279] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
KERNEL[2320.870421] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
KERNEL[2320.870556] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
KERNEL[2320.870714] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
KERNEL[2320.871437] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
KERNEL[2320.871611] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
UDEV  [2320.900256] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
UDEV  [2320.903328] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
UDEV  [2320.904157] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
UDEV  [2320.905639] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
UDEV  [2320.905989] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
UDEV  [2320.907385] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
UDEV  [2320.909369] unbind   /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
UDEV  [2320.910771] remove   /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
KERNEL[2324.093851] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
KERNEL[2324.095439] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
KERNEL[2324.096619] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
KERNEL[2324.096829] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
KERNEL[2324.097630] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
KERNEL[2324.097843] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
KERNEL[2324.097925] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
KERNEL[2324.098018] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
UDEV  [2324.111345] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
UDEV  [2324.116155] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
UDEV  [2324.116526] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
UDEV  [2324.119275] add      /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
UDEV  [2324.127865] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.2 (usb)
UDEV  [2324.138537] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0 (usb)
UDEV  [2324.145872] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.1 (usb)
UDEV  [2324.153251] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-3 (usb)
</pre>

### Journal messages whilst un/plugging keyboard
<code>journalctl -f -n 0</code>
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
Nov 29 10:45:18 pizero2w echo[3505]: pracmon: Sending USR1 signal to pmZero.py
Nov 29 10:45:18 pizero2w (udev-worker)[3455]: card0: Process '/home/rob/proj/practiceMonitor/udev/trigger.sh' failed with exit code 1.
</pre>
