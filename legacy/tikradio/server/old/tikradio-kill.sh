#!/bin/bash
set -eu
. ~/.tikradiorc
touch "$KILLFILE"
./tikradio-skip.sh
rm -f -- "$KILLFILE"
rm -f -- "$TMP/tikp"*
: > "$PUTKI"
exit 0
