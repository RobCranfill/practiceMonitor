#!/bin/bash
# this is the script the udev rule calls

python_file="pmZero.py"

logfile="/home/rob/proj/practiceMonitor/udev/udev.log"

# echo -n `date` >>$logfile
# echo "; $SUBSYSTEM; $ACTION"  >>$logfile

if [ "$ACTION" = "change" ]; then
  systemd-cat echo "cran: Sending USR1 signal to $python_file"
  systemd-cat echo "cran: PIDs: `pgrep $python_file`"
  pkill --signal USR1 --full $python_file
  exit 0
fi
