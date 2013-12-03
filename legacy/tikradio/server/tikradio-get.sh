#!/bin/bash
set -eu
. ~/.tikradiorc

if $OLDERTHAN 300 $TMP/tikplaystreaming; then
	echo skip | . tikradio-ctl.sh >/dev/null 2>/dev/null
fi

file="`tempfile -d $TMP -p tikp`"
date="`date +%y%m%d-%H%M%S`"

#echo "100 DOWNLOAD"
nice -n 19 dd bs=1k count=25000 of="$file" >/dev/null 2>/dev/null
hash="`$HASHER "$file"`"

#Filtteri
if grep -q "$hash" "$BANFILE"; then
    rm "$file"
    exit 0
fi

#!kakkosnappi
if [ "$#" -lt 1 ]; then

#Topten logitus
size="`stat -c "%s" "$file"`"
echo "$date" "$hash" "$size" >> $LOGI

#Topten hankkija
if grep -q "$hash" "$TOPTENLIST"; then
    if [ ! -e "$TOPTENDIR"/"$hash" ]; then
      cp "$file" "$TOPTENDIR"/"$hash" || true
      oldfile="`find "$TOPTENDIR" -type file -print | grep -v -f "$TOPTENLIST" | head -1`"
      [ -f "$oldfile" ] && rm "$oldfile" || true
    fi
fi

fi #!kakkosnappi

# kirjoitetaan putkeen
echo "$file" >>$PUTKI
touch "$file"

exit 0
