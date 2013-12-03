#!/bin/bash
set -eu
. ~/.tikradiorc
ulimit -v 5000
command="`head -1`"
case "$command" in
kill*) nohup ./tikradio-kill.sh; #echo "240 OK!"
skip*) ./tikradio-skip.sh; #echo "250 OK!"
*) echo "Usage: RTFM!"; #echo "3.1415926535897932384626433 Failure!"
esac
echo "OK"
exit 0
