#!/bin/bash
# for PraciceMonitor project
# this is the script the udev rule calls

python_file="pmZero.py"

# we now filter for only 'change' actions in the rule.
# if [ "$ACTION" = "change" ]; then

systemd-cat echo "pracmon: Sending USR1 signal to $python_file; PIDs `pgrep --full $python_file` - $1"

pkill --signal USR1 --full $python_file
exit 0

#fi
