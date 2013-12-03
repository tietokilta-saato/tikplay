#!/bin/bash
set -eu
if (("$UID" != "19564"));
then echo "Please run only as tikplay."
exit 1
fi
cd ~/tikradio
./stop.sh
sleep 1
./start.sh
exit 0
