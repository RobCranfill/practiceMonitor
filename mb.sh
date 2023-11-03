#/bin/bash
# send MIDI data thru Python program

HW_ADDR=`amidi -l  | grep MPKmini2 | awk '{print $2}'`

amidi -d -p $HW_ADDR | python3 midiBit.py

