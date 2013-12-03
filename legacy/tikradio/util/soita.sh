#!/bin/bash
set -eu
. ~/.tikradiorc

case "$1" in
    http://*ogg)
    :> "$TMP/tikplaystreaming"
    exec $OGG123 $OGG123_OPTS "$1" ;;
    http://*)
    :> "$TMP/tikplaystreaming"
    exec $MPG123 $MPG123_OPTS "$1" ;;
    *)
    case `$FILE_CMD "$1"` in
	*Ogg*)
	exec $OGG123 $OGG123_OPTS $1 ;;
	*odule\ sound*)
        exec $PLAYMOD "$1" ;;
	*SID*)
        exec $PLAYSID "$1" ;;
	*text*)
        exec $FESTIVAL "$1" ;;
	*)
	exec $MPG123 $MPG123_OPTS $1
    esac 
    #if file "$1" |grep "Ogg" > /dev/null; then
    #	exec $OGG123 $OGG123_OPTS $1
    #else
    #	exec $MPG123 $MPG123_OPTS $1
    #fi    
esac
