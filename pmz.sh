#!/bin/bash
# run pmZero from the command line

echo "Checking service..."
systemctl is-active pmz.service
if [ $? -eq 0 ] 
then 
  echo "The service is running?"
  echo "stop it, then try again"
  exit 1 
fi

python pmZero.py
