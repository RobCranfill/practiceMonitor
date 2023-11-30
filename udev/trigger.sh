#!/bin/bash
# for PraciceMonitor project
# this is the script the udev rule calls

python_file="pmZero.py"
# logfile="/home/rob/proj/practiceMonitor/udev/udev.log"
# echo "udev rule fired `date`; $SUBSYSTEM; $ACTION"  >>$logfile

# we now filter for only 'change' actions in the rule.
# if [ "$ACTION" = "change" ]; then

#  echo "udev action is 'change'." >>$logfile

  systemd-cat echo "pracmon: Sending USR1 signal to $python_file; PIDs `pgrep --full $python_file`"
  pkill --signal USR1 --full $python_file
  exit 0

#fi
