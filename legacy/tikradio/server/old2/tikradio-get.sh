#!/bin/bash
set -eu
. ~/.tikradiorc

if $OLDERTHAN 300 $TMP/tikplaystreaming; then
	echo skip | . tikradio-ctl.sh >/dev/null 2>/dev/null
fi

file="`tempfile $TMP/tikpXXXXXX`"
date="`date +%y%m%d-%H%M%S`"

#echo "100 DOWNLOAD"
nice -n 19 dd bs=1k count=25000 of="$file" >/dev/null 2>/dev/null

hash="`$HASHER "$file"`"

if [ "$#" -lt 1 ]; then
size="`/sbin/stat -q -s "$file"`"
echo "$date" "$hash" "$size" >> $LOGI
$PSEUDORANDOM || cp "$file" ~/music/kakkosnappi.musaa || true
fi

#Filtteri
if grep -q "$hash" "$BANFILE"; then
#    echo "505 SCHEIBE!11"
    rm "$file"
    exit 0
fi

# kirjoitetaan putkeen
echo "$file" >>$PUTKI
touch "$file"
exit 0
