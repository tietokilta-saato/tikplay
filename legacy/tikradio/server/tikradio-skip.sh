#!/bin/bash
set -u
. ~/.tikradiorc
kill "`cat $SOITAPID`" >/dev/null 2>/dev/null; :> $SOITAPID 
exit 0
