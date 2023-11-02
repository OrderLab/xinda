set -m
program_pid=$(ps aux | grep "python /tmp/ycsb" | grep -v grep | awk '{print $2}')
while ps -p $program_pid > /dev/null; do
	echo "Still executing, sleep 10s"
	# Sleep for 1 second and increment the current time
	sleep 10
done
