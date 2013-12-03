#!/bin/bash
set -eu
. ~/.tikradiorc
#ulimit -v 5000
command="`head -1`"
case "$command" in
kill*) nohup ./tikradio-kill.sh;;
skip*) ./tikradio-skip.sh;;
http*) echo "$command" >> $PUTKI;;
kirma*) nohup /home/sslaitin/kirma4.sh;;
*) echo "Usage: RTFM!";;
esac
echo "OK"
exit 0
