echo starting

nohup uwsgi uwsgi.ini &

echo $! > myback_pid.txt

echo started
