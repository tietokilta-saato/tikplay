#!/bin/bash
set -eu
. ~/.tikradiorc
if test -e "$RUNNING"; then echo "Error: TiKradio already running!"; exit
1; fi
touch "$RUNNING"

# ESound
#/usr/freeware/bin/esd -nobeeps -unix -r 48000 & echo $! > $ESDPID

rm -f -- "$TMP/tikp"* "$KILLFILE"
: > "$PUTKI"

# Main loop
./tikradio.sh & echo $! > $PIDFILE

# daemon init (getfile.sh)
nice -n 19 mini-inetd "$GETPORT" ./tikradio-get.sh & echo $! > $GETPID

# daemon init (control.sh)
nice -n 19 mini-inetd "$CTLPORT" ./tikradio-ctl.sh & echo $! > $CTLPID

# daemon init (mouse.sh)
#./savepid "$SERIALPID" ./serial "$SERIAL_PORT" | ./tikradio-mouse.sh &

#echo "TiKradio started"
exit 0
