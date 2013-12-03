#!/bin/bash
set -eu
. ~/.tikradiorc
file="`tempfile -d $TMP -p tikp`"
#echo "100 DOWNLOAD"
nice -n 19 dd bs=1k count=10240 of="$file" >/dev/null 2>/dev/null
#Filtteri
if grep -q `$HASHER "$file"` "$BANFILE"; then
#    echo "505 SCHEIBE!11"
    rm "$file"
    exit 0
#if grep -q "`$HASHER "$file" | cut -f 1 -d ' '`" "$FUNFILE"; then
#    counter=50
#else
#    counter=1
#echo "666 OK!"
# kirjoitetaan lokiin
echo "$file" >>$PUTKI
touch "$file"
exit 0
