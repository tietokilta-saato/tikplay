#!/bin/bash
set -eu
if (("$UID" != "19564"));
then echo "Please run only as tikplay."
exit 1
fi
~/tikradio/init.sh
cd ~/tikradio/server/
#perl -e 'use POSIX; POSIX::close(0); POSIX::close(1); POSIX::close(2); setsid(); exec("./tikradio-start.sh");' 
./tikradio-start.sh
exit 0
