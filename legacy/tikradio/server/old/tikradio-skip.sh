#!/bin/bash
set -eu
. ~/.tikradiorc
kill "`cat $OGGPID`" >/dev/null 2>/dev/null
exit 0
