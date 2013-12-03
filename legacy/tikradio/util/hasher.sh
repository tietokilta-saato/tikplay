#!/bin/sh
dd if="$1" bs=1024 count=100 2>/dev/null | /usr/bin/md5sum | \
cut -f 1 -d ' '
