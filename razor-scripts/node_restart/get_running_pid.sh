set -m
program_pid=$(ps -u ruiming -o pid,user,cmd,etime | grep "java" | grep -v "grep" | awk '{split($4, time, ":"); if (time[1] < 5) print $1}')
echo $program_pid
