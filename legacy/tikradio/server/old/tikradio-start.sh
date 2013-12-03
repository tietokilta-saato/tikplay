#!/bin/bash
set -eu
. ~/.tikradiorc
if test -e "running"; then echo "Error: TiKradio already running!"; exit
1; fi
touch "running"
rm -f -- "$TMP/tikp"*
: > "$PUTKI"
./tikradio.sh & echo $! > $PIDFILE
# daemon init (getfile.sh)
nice mini-inetd "$GETPORT" ./tikradio-get.sh & echo $! > $GETPID
# daemon init (control.sh)
mini-inetd "$CTLPORT" ./tikradio-ctl.sh & echo $! > $CTLPID
#echo "TiKradio started"
exit 0
