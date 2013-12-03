#!/bin/bash
set -eu
if (("$UID" != "19564"));
then echo "Please run only as tikplay."
exit 1
fi
cd ~/tikradio/server/
./tikradio-stop.sh
exit 0
