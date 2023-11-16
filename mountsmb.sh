#!/bin/bash
# mount the pi via samba so I can work on it with VSCode

PWVAR=`cat pw.text`
sudo mount -t cifs -o username=rob,password=$PWVAR,uid=1000,rw //pizero2w.local/home /mnt/pizero2w

ls -al /mnt/pizero2w/proj/practiceMonitor

cd /mnt/pizero2w/proj/practiceMonitor
code .
