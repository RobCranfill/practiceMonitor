#!/bin/bash
# run pmZero from the command line

echo "Checking service..."
systemctl is-active pmz.service
if [ $? -eq 0 ]
then
  echo "The service is running?"
  echo "Stop it, then try again!"
  exit 1
fi
echo "Service NOT running - OK!"

python pmZero.py `cat aio_secret.text`

# Turn LCD off - app should do this but it doesn't!
echo Setting backlight off in main script - FIXME!
python /home/rob/.local/bin/LCD_util.py off
