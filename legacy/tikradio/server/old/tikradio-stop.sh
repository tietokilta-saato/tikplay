#!/bin/bash
set -eu
. ~/.tikradiorc
if test ! -e "running"; then echo "Error: TiKradio not running!"; exit
1; fi
kill "`cat $CTLPID`" >/dev/null 2>/dev/null; : > $CTLPID
kill "`cat $GETPID`" >/dev/null 2>/dev/null; : > $GETPID
killall tikradio.sh >/dev/null 2>/dev/null; : > $PIDFILE
killall tail >/dev/null 2>/dev/null; : > $TAILPID
killall "$SOITA" >/dev/null 2>/dev/null; : >$OGGPID
rm "running"
#echo "TiKradio stopped"
exit 0
