#!/bin/bash
set -eu
. ~/.tikradiorc
count=`ls "$TOPTENDIR"| wc -l`
for i in 1 2 3 
do rand=`perl -e "print rand()*100000%$count+1"` 
file="`ls \"$TOPTENDIR\" | head -$rand | tail -1`"
./tikradio-get.sh -topten < "$TOPTENDIR/$file" >/dev/null 2>/dev/null &
done
exit 0
