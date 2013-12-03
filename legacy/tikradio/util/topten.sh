#!/bin/bash
set -eu
. ~/.tikradiorc
#cut -d' ' -f2 $LOGI| sort|uniq -c| sort -n | tail -10 | sed 's/^.* \([^ ]*\)$/\1/' > $TOPTENLIST
tail -4700 $LOGI | cut -d' ' -f2 | sort|uniq -c| sort -n | tail -20 | awk '{ print $2; }' > $TOPTENLIST
