#!/bin/bash
set -eu
. ~/.tikradiorc
touch "$KILLFILE"
./tikradio-skip.sh
rm -f -- "$TMP/tikp"*
kill "`cat $TAILPID`" >/dev/null 2>/dev/null; :> "$TAILPID"
exit 0
