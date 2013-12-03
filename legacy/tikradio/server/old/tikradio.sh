#!/bin/bash
set -eu
. ~/.tikradiorc
while true; do
./savepid $TAILPID tail -f $PUTKI | \
  { while [ ! -e $KILLFILE ]; do read file || exit 0; \
    $SOITA $SOITA_OPTS "$file" >/dev/null 2>/dev/null & echo $! > $OGGPID; wait >/dev/null 2>/dev/null; \
    rm -f -- "$file";done }
done
