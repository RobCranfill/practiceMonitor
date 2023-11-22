#!/bin/bash
# start, stop, check the service
# arg[1] = {"start", "stop", "status", "enable", "disable"}

if [ "$#" -ne 1 ]; then
    echo '{"enable", "disable", "start", "stop", "status"}'
    exit 1
fi

sudo systemctl $1 pmz.service
