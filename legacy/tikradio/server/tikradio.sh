#!/bin/bash
set -u
. ~/.tikradiorc
while true; do
:> "$PUTKI"
rm -f -- "$KILLFILE"
./savepid $TAILPID tail -f $PUTKI | \
  { while [ ! -e $KILLFILE ]; do read file || exit 0; \
    ln -sf "$file" "$HOME/music/now-playing.musaa"; \
    $SOITA $SOITA_OPTS "$file" >/dev/null 2>$SOITA_OUT & echo $! > $SOITAPID; \
    wait >/dev/null 2>/dev/null; \
    rm -f -- "$file" "$TMP/tikplaystreaming"; \
    "$HOME/tikradio/util/resethw.sh" ;done }
done
