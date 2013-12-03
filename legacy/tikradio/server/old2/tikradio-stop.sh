#!/bin/bash
set -u
. ~/.tikradiorc
if test ! -e "$RUNNING"; then echo "Error: TiKradio not running!"; exit 0; fi
touch "$KILLFILE"
kill "`cat $CTLPID`" >/dev/null 2>/dev/null; : > $CTLPID 
kill "`cat $GETPID`" >/dev/null 2>/dev/null; : > $GETPID
kill "`cat $SERIALPID`" >/dev/null 2>/dev/null; : >$SERIALPID

kill "`cat $PIDFILE`" >/dev/null 2>/dev/null; : > $PIDFILE
kill "`cat $TAILPID`" >/dev/null 2>/dev/null; : > $TAILPID
kill "`cat $SOITAPID`" >/dev/null 2>/dev/null; : >$SOITAPID

kill "`cat $ESDPID`" >/dev/null 2>/dev/null; : > $ESDPID
rm -f -- "$RUNNING"
#echo "TiKradio stopped"
exit 0
