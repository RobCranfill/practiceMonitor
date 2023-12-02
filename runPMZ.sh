#!/bin/bash
# Run the Performance Monitor as a service.

cd /home/rob/proj/practiceMonitor
echo "PerfMon started" >>./perfmon.log
source ./zenv/bin/activate
python ./pmZero.py `cat aio_secret.text`
echo "PerfMon ended" `date` >>./perfmon.log
