#!/bin/bash
# Run the Performance Monitor as a service ?

echo "PerfMon started" >>perfmon.log

cd /home/rob/proj/practiceMonitor

source ./zenv/bin/activate

python ./pmZero.py

echo done!
echo "PerfMon ended" `date` >>perfmon.log

