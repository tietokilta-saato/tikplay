#!/bin/bash
set -eu
. ~/.tikradiorc
ulimit -v 5000
while read command
do
case "$command" in
STATUS:\ 3*) if [ "`ls ~/tmp/ | wc -l`" -ge 1 ]; then
  cp ~/music/now-playing.musaa ~/music/kakkosnappi.musaa || true
fi;;
STATUS:\ 2*) if [ "`ls ~/tmp/ | wc -l`" -le 1 ]; then
  ./tikradio-get.sh -mouse < ~/music/kakkosnappi.musaa >/dev/null 2>/dev/null &
fi;;
STATUS:\ 1*) ./tikradio-skip.sh;;
*) echo "Usage: RTFM!";;
esac
done
echo "OK"
exit 0
