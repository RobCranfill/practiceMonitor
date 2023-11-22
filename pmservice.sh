#!/bin/bash
# start, stop, check the service
# arg[1] = {"start", "stop", "status", "enable", "disable"}

if [ "$#" -ne 1 ]; then
    echo '{"start", "stop", "status", "enable", "disable"}'
    exit 1
fi

systemctl $1 pmz.service
