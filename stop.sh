echo stopping

kill -9 `cat myback_pid.txt`
rm -f myback_pid.txt

echo stopped
