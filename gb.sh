#/bin/bash
# send MIDI data thru Python program

amidi -d -p hw:0,0,0 | python3 b.py

