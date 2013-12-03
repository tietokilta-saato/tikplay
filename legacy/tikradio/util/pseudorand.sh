#!/bin/bash
set -eu
. ~/.tikradiorc
i=`cat "$RANDOM_SEED_FILE"`
echo "$i + 1" | bc > "$RANDOM_SEED_FILE"
exit `echo "($i % 19) * ($i % 29) == 0" |bc`
