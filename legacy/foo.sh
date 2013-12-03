#!/bin/bash
uptime
ps -o 'tty pid ppid nice pcpu stime etime args' -u tikradio f |grep -v ^pts |grep -v defunct |grep -v sshd
echo " "
echo "files in tmp"
echo " "
ls -lth ~/tmp/
echo " "
echo "currently downloading from:"
echo " "
netstat -a | grep '\.5000.*ESTABLISHED'
echo "Now playing:"
tail -5 ~/run/tikradio-player.out

